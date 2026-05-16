# ============================================================
# payment.py  SmartCare Payment Management Module
# ============================================================
import sqlite3, hmac, hashlib, os, json, secrets, smtplib, threading
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from functools import wraps
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

from dotenv import load_dotenv
load_dotenv()
import razorpay

RAZORPAY_KEY_ID     = os.environ.get('RAZORPAY_KEY_ID',     'rzp_test_PLACEHOLDER')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'test_secret_PLACEHOLDER')

VALID_COUPONS = {'HEALTH10':10,'CARE20':20,'FIRST50':50,'SMARTCARE':15}

def get_db():
    conn = sqlite3.connect('medical.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first','warning')
            return redirect(url_for('signin_as'))
        return f(*args, **kwargs)
    return decorated

def init_payment_tables():
    conn = get_db(); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, doctor_id INTEGER NOT NULL,
        appointment_id INTEGER, razorpay_order_id TEXT,
        razorpay_payment_id TEXT, razorpay_signature TEXT,
        amount REAL NOT NULL, currency TEXT DEFAULT 'INR',
        payment_status TEXT DEFAULT 'pending', payment_method TEXT,
        coupon_code TEXT, discount_amount REAL DEFAULT 0,
        final_amount REAL, receipt_number TEXT UNIQUE, notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payment_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, payment_id INTEGER NOT NULL,
        event_type TEXT, event_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL, balance REAL DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS wallet_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL,
        amount REAL NOT NULL, type TEXT, description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    for col in [("payment_status","TEXT DEFAULT 'unpaid'"),("payment_id","INTEGER"),("mode","TEXT DEFAULT 'online'")]:
        try: c.execute(f"ALTER TABLE appointments ADD COLUMN {col[0]} {col[1]}")
        except: pass
    conn.commit(); conn.close()
    print("[Payment] Tables initialised")

def generate_receipt():
    return f"RCP-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(4).upper()}"

def verify_razorpay_signature(order_id, payment_id, signature):
    msg = f"{order_id}|{payment_id}".encode()
    expected = hmac.new(RAZORPAY_KEY_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def send_payment_email(to_email, patient_name, doctor_name, amount,
                       appointment_date, appointment_time, mode, receipt_no, video_link=None):
    gmail_user = os.environ.get('GMAIL_USER','').strip()
    gmail_pass = os.environ.get('GMAIL_PASSWORD','').strip()
    if not gmail_user or not gmail_pass: return
    subject = f"Payment Confirmed - SmartCare #{receipt_no}"
    video_section = f"\nVideo Link: {video_link}" if video_link else ""
    body = f"Dear {patient_name},\n\nAppointment confirmed!\n\nReceipt: {receipt_no}\nDoctor: Dr. {doctor_name}\nDate: {appointment_date}\nTime: {appointment_time}\nMode: {mode}\nAmount: Rs.{amount:.2f}\nStatus: PAID{video_section}\n\nThank you,\nSmartCare Team"
    def _send():
        try:
            msg = MIMEMultipart(); msg['Subject']=subject; msg['From']=f"SmartCare <{gmail_user}>"; msg['To']=to_email
            msg.attach(MIMEText(body,'plain'))
            with smtplib.SMTP('smtp.gmail.com',587,timeout=15) as s:
                s.ehlo(); s.starttls(); s.login(gmail_user,gmail_pass); s.sendmail(gmail_user,[to_email],msg.as_string())
        except Exception as e: print(f"[Payment] Email error: {e}")
    threading.Thread(target=_send,daemon=True).start()

@payment_bp.route('/checkout/<int:appointment_id>')
@login_required
def checkout(appointment_id):
    conn = get_db()
    apt = conn.execute('''SELECT a.*,u.name AS patient_name,u.email AS patient_email,
        du.name AS doctor_name,d.consultation_fee,d.specialization,d.id AS doc_id
        FROM appointments a JOIN patients p ON a.patient_id=p.id JOIN users u ON p.user_id=u.id
        JOIN doctors d ON a.doctor_id=d.id JOIN users du ON d.user_id=du.id WHERE a.id=?''',(appointment_id,)).fetchone()
    if not apt: conn.close(); flash('Appointment not found','danger'); return redirect(url_for('patient_dashboard'))
    wallet = conn.execute('SELECT balance FROM wallets WHERE user_id=?',(session['user_id'],)).fetchone()
    wallet_balance = wallet['balance'] if wallet else 0.0
    conn.close()
    return render_template('payment/checkout.html',apt=apt,fee=apt['consultation_fee'],
        wallet_balance=wallet_balance,razorpay_key=RAZORPAY_KEY_ID)

@payment_bp.route('/apply-coupon',methods=['POST'])
@login_required
def apply_coupon():
    data=request.get_json(); code=(data.get('coupon','') or '').upper().strip(); amount=float(data.get('amount',0))
    if code in VALID_COUPONS:
        pct=VALID_COUPONS[code]; discount=round(amount*pct/100,2); final=round(amount-discount,2)
        return jsonify({'success':True,'discount':discount,'final':final,'percent':pct,'code':code})
    return jsonify({'success':False,'message':'Invalid coupon code'})

@payment_bp.route('/create-order',methods=['POST'])
@login_required
def create_order():
    try:
        data=request.get_json(); appointment_id=int(data.get('appointment_id'))
        coupon_code=(data.get('coupon_code','') or '').upper().strip()
        use_wallet=bool(data.get('use_wallet',False))
        conn=get_db()
        apt=conn.execute('''SELECT a.*,d.consultation_fee,d.id AS doc_id,du.name AS doctor_name
            FROM appointments a JOIN doctors d ON a.doctor_id=d.id JOIN users du ON d.user_id=du.id
            WHERE a.id=?''',(appointment_id,)).fetchone()
        if not apt: conn.close(); return jsonify({'success':False,'error':'Appointment not found'})
        base_amount=float(apt['consultation_fee']); discount_amount=0.0
        if coupon_code in VALID_COUPONS:
            pct=VALID_COUPONS[coupon_code]; discount_amount=round(base_amount*pct/100,2)
        final_amount=round(base_amount-discount_amount,2)
        wallet_used=0.0
        if use_wallet:
            wallet=conn.execute('SELECT balance FROM wallets WHERE user_id=?',(session['user_id'],)).fetchone()
            if wallet and wallet['balance']>0:
                wallet_used=min(wallet['balance'],final_amount); final_amount=round(final_amount-wallet_used,2)
        receipt_no=generate_receipt()
        
        # Create Razorpay Order
        if RAZORPAY_KEY_ID != 'rzp_test_PLACEHOLDER':
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            rzp_order = client.order.create({
                'amount': int(final_amount * 100),
                'currency': 'INR',
                'receipt': receipt_no,
                'payment_capture': 1
            })
            order_id = rzp_order['id']
        else:
            order_id = f"order_{secrets.token_hex(10)}"

        conn.execute('''INSERT INTO payments(user_id,doctor_id,appointment_id,razorpay_order_id,
            amount,final_amount,discount_amount,coupon_code,receipt_number,payment_status)
            VALUES(?,?,?,?,?,?,?,?,?,'pending')''',
            (session['user_id'],apt['doc_id'],appointment_id,order_id,
             base_amount,final_amount,discount_amount,coupon_code or None,receipt_no))
        conn.commit()
        if wallet_used>0:
            conn.execute('UPDATE wallets SET balance=balance-?,updated_at=CURRENT_TIMESTAMP WHERE user_id=?',(wallet_used,session['user_id']))
            conn.execute("INSERT INTO wallet_transactions(user_id,amount,type,description) VALUES(?,?,'debit','Used for appointment')",(session['user_id'],wallet_used))
            conn.commit()
        conn.close()
        return jsonify({'success':True,'order_id':order_id,'amount':int(final_amount*100),
            'currency':'INR','receipt':receipt_no,'key':RAZORPAY_KEY_ID,
            'name':session.get('name','Patient'),'doctor':apt['doctor_name'],'wallet_used':wallet_used})
    except Exception as e:
        print(f"[Payment] create_order error: {e}"); return jsonify({'success':False,'error':str(e)})

@payment_bp.route('/verify',methods=['POST'])
@login_required
def verify_payment():
    try:
        data=request.get_json(); order_id=data.get('razorpay_order_id','')
        payment_id=data.get('razorpay_payment_id',''); signature=data.get('razorpay_signature','')
        apt_id=int(data.get('appointment_id',0))
        is_test=RAZORPAY_KEY_ID=='rzp_test_PLACEHOLDER'
        sig_ok=is_test or verify_razorpay_signature(order_id,payment_id,signature)
        if not sig_ok: return jsonify({'success':False,'error':'Signature verification failed'})
        conn=get_db()
        conn.execute('''UPDATE payments SET razorpay_payment_id=?,razorpay_signature=?,
            payment_status='paid',payment_method=?,updated_at=CURRENT_TIMESTAMP
            WHERE razorpay_order_id=?''',(payment_id,signature,data.get('method','razorpay'),order_id))
        conn.execute("UPDATE appointments SET status='confirmed',payment_status='paid' WHERE id=?",(apt_id,))
        conn.execute('''INSERT INTO payment_transactions(payment_id,event_type,event_data)
            SELECT id,'payment_captured',? FROM payments WHERE razorpay_order_id=?''',(json.dumps(data),order_id))
        row=conn.execute('''SELECT p.receipt_number,p.final_amount,a.appointment_date,a.appointment_time,a.mode,
            u.name AS patient_name,u.email AS patient_email,du.name AS doctor_name
            FROM payments p JOIN appointments a ON p.appointment_id=a.id
            JOIN users u ON p.user_id=u.id JOIN doctors d ON p.doctor_id=d.id JOIN users du ON d.user_id=du.id
            WHERE p.razorpay_order_id=?''',(order_id,)).fetchone()
        conn.commit(); conn.close()
        if row:
            mode=row['mode'] or 'online'; video_link=None
            if mode=='online': video_link=f"https://meet.jit.si/smartcare-{apt_id}-{secrets.token_hex(4)}"
            send_payment_email(row['patient_email'],row['patient_name'],row['doctor_name'],
                row['final_amount'],row['appointment_date'],row['appointment_time'],
                mode,row['receipt_number'],video_link)
            return jsonify({'success':True,'receipt':row['receipt_number'],'video_link':video_link,
                'redirect':url_for('payment.success',appointment_id=apt_id)})
        return jsonify({'success':True,'redirect':url_for('payment.success',appointment_id=apt_id)})
    except Exception as e:
        print(f"[Payment] verify error: {e}"); return jsonify({'success':False,'error':str(e)})

@payment_bp.route('/success/<int:appointment_id>')
@login_required
def success(appointment_id):
    conn=get_db()
    row=conn.execute('''SELECT p.*,a.appointment_date,a.appointment_time,a.mode,
        du.name AS doctor_name,d.specialization,u.name AS patient_name
        FROM payments p JOIN appointments a ON p.appointment_id=a.id
        JOIN doctors d ON p.doctor_id=d.id JOIN users du ON d.user_id=du.id
        JOIN users u ON p.user_id=u.id
        WHERE p.appointment_id=? AND p.payment_status='paid'
        ORDER BY p.id DESC LIMIT 1''',(appointment_id,)).fetchone()
    conn.close()
    if not row: flash('Payment record not found','warning'); return redirect(url_for('patient_dashboard'))
    mode=row['mode'] or 'online'
    video_link=f"https://meet.jit.si/smartcare-{appointment_id}" if mode=='online' else None
    return render_template('payment/success.html',row=row,video_link=video_link)

@payment_bp.route('/failed/<int:appointment_id>')
@login_required
def failed(appointment_id):
    return render_template('payment/failed.html',appointment_id=appointment_id)

@payment_bp.route('/history')
@login_required
def history():
    conn=get_db()
    payments=conn.execute('''SELECT p.*,a.appointment_date,a.appointment_time,a.mode,
        du.name AS doctor_name,d.specialization
        FROM payments p LEFT JOIN appointments a ON p.appointment_id=a.id
        LEFT JOIN doctors d ON p.doctor_id=d.id LEFT JOIN users du ON d.user_id=du.id
        WHERE p.user_id=? ORDER BY p.created_at DESC''',(session['user_id'],)).fetchall()
    wallet=conn.execute('SELECT balance FROM wallets WHERE user_id=?',(session['user_id'],)).fetchone()
    wallet_balance=wallet['balance'] if wallet else 0.0
    total_paid=sum(r['final_amount'] or 0 for r in payments if r['payment_status']=='paid')
    conn.close()
    return render_template('payment/history.html',payments=payments,wallet_balance=wallet_balance,total_paid=total_paid)

@payment_bp.route('/receipt/<int:payment_id>')
@login_required
def download_receipt(payment_id):
    conn=get_db()
    row=conn.execute('''SELECT p.*,a.appointment_date,a.appointment_time,a.mode,
        du.name AS doctor_name,d.specialization,u.name AS patient_name,u.email AS patient_email
        FROM payments p JOIN appointments a ON p.appointment_id=a.id
        JOIN doctors d ON p.doctor_id=d.id JOIN users du ON d.user_id=du.id
        JOIN users u ON p.user_id=u.id
        WHERE p.id=? AND p.user_id=?''',(payment_id,session['user_id'])).fetchone()
    conn.close()
    if not row: flash('Receipt not found','danger'); return redirect(url_for('payment.history'))
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO
        buf=BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4); styles=getSampleStyleSheet(); elems=[]
        elems.append(Paragraph("SmartCare - Payment Receipt",styles['Title'])); elems.append(Spacer(1,12))
        data=[['Field','Details'],['Receipt No',row['receipt_number']],['Patient',row['patient_name']],
            ['Doctor',f"Dr. {row['doctor_name']}"],['Specialization',row['specialization']],
            ['Date',row['appointment_date']],['Time',row['appointment_time']],
            ['Mode',(row['mode'] or 'online').capitalize()],['Base Amount',f"Rs.{row['amount']:.2f}"],
            ['Discount',f"Rs.{row['discount_amount'] or 0:.2f}"],['Amount Paid',f"Rs.{row['final_amount']:.2f}"],
            ['Status',row['payment_status'].upper()],['Payment ID',row['razorpay_payment_id'] or 'N/A'],
            ['Date Paid',str(row['created_at'])[:16]]]
        t=Table(data,colWidths=[180,300])
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#667eea')),
            ('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f2f8')]),
            ('GRID',(0,0),(-1,-1),0.5,colors.grey),('FONTSIZE',(0,0),(-1,-1),10),('PADDING',(0,0),(-1,-1),8)]))
        elems.append(t); elems.append(Spacer(1,20))
        elems.append(Paragraph("Thank you for choosing SmartCare!",styles['Normal']))
        doc.build(elems); buf.seek(0)
        resp=make_response(buf.read())
        resp.headers['Content-Type']='application/pdf'
        resp.headers['Content-Disposition']=f'attachment; filename=receipt_{row["receipt_number"]}.pdf'
        return resp
    except ImportError:
        flash('ReportLab not installed. Run: pip install reportlab','warning')
        return redirect(url_for('payment.history'))

@payment_bp.route('/refund/<int:payment_id>',methods=['POST'])
@login_required
def request_refund(payment_id):
    conn=get_db()
    pay=conn.execute('SELECT * FROM payments WHERE id=? AND user_id=?',(payment_id,session['user_id'])).fetchone()
    if not pay or pay['payment_status']!='paid':
        conn.close(); return jsonify({'success':False,'error':'Refund not applicable'})
    conn.execute('INSERT OR IGNORE INTO wallets(user_id,balance) VALUES(?,0)',(session['user_id'],))
    conn.execute('UPDATE wallets SET balance=balance+?,updated_at=CURRENT_TIMESTAMP WHERE user_id=?',(pay['final_amount'],session['user_id']))
    conn.execute("INSERT INTO wallet_transactions(user_id,amount,type,description) VALUES(?,?,'credit','Refund for cancelled appointment')",(session['user_id'],pay['final_amount']))
    conn.execute("UPDATE payments SET payment_status='refunded' WHERE id=?",(payment_id,))
    if pay['appointment_id']:
        conn.execute("UPDATE appointments SET status='cancelled',payment_status='refunded' WHERE id=?",(pay['appointment_id'],))
    conn.commit(); conn.close()
    flash(f"Rs.{pay['final_amount']:.2f} refunded to your SmartCare wallet.",'success')
    return jsonify({'success':True})

@payment_bp.route('/wallet/topup',methods=['POST'])
@login_required
def wallet_topup():
    amount=float(request.form.get('amount',0))
    if amount<=0 or amount>10000: flash('Invalid amount','danger'); return redirect(url_for('payment.history'))
    conn=get_db()
    conn.execute('INSERT OR IGNORE INTO wallets(user_id,balance) VALUES(?,0)',(session['user_id'],))
    conn.execute('UPDATE wallets SET balance=balance+?,updated_at=CURRENT_TIMESTAMP WHERE user_id=?',(amount,session['user_id']))
    conn.execute("INSERT INTO wallet_transactions(user_id,amount,type,description) VALUES(?,?,'credit','Wallet top-up')",(session['user_id'],amount))
    conn.commit(); conn.close()
    flash(f'Rs.{amount:.2f} added to your SmartCare wallet!','success')
    return redirect(url_for('payment.history'))