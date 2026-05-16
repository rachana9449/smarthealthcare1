# Payment Gateway & Email Setup Guide

Follow these steps to fully configure the SmartCare online payment system and email notifications for doctor appointment bookings.

## 1. Razorpay Payment Gateway Setup
SmartCare uses Razorpay to securely process payments for doctor appointments. It supports UPI, Net Banking, Credit/Debit Cards, and Wallets.

### Get Your API Keys
1. Go to the [Razorpay Dashboard](https://dashboard.razorpay.com/) and create an account or log in.
2. Ensure you are in **Test Mode** (toggle is usually at the top right).
3. Navigate to **Settings -> API Keys**.
4. Click on **Generate Key** (or Generate Test Key).
5. You will see a `Key Id` and `Key Secret`. Do not share these publicly.

### Configure Application
1. In your SmartCare project directory (`c:\smarthealthcare1\smarthealthcare`), open the `.env` file (or create one if it doesn't exist).
2. Add your Razorpay credentials to the file:
```env
RAZORPAY_KEY_ID=your_key_id_here
RAZORPAY_KEY_SECRET=your_key_secret_here
```

## 2. SMTP Email Configuration
The system sends automatic email notifications and video consultation links upon successful payment.

### Get Gmail App Password
If you are using Gmail, standard passwords no longer work for SMTP. You must create an App Password:
1. Go to your Google Account -> **Security**.
2. Ensure **2-Step Verification** is turned on.
3. Search for **App passwords** in your Google Account search bar.
4. Create a new App Password (name it "SmartCare App" or similar).
5. Copy the 16-character generated password.

### Configure Application
1. Open the `.env` file again.
2. Add your Gmail credentials:
```env
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_16_character_app_password
```

## 3. Environment Installation
Ensure all dependencies are installed, including the newly added Razorpay module.

Open your terminal, navigate to the project directory, and run:
```bash
pip install -r requirements.txt
```

## 4. Run the Application
The `init_payment_tables()` function will automatically create the necessary SQLite tables (`payments`, `payment_transactions`, `wallets`, `wallet_transactions`) and modify the `appointments` table when you start the server.

Start the Flask application:
```bash
python app.py
```

Your patients will now see the "Proceed to Payment" button when booking and "Pay Now" on their dashboard for any unpaid appointments!
