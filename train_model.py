"""
Train Machine Learning Model for Disease Prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Sample disease-symptom dataset
data = {
    'symptoms': [
        'fever, headache, body pain',
        'fever, cough, fatigue',
        'chest pain, shortness of breath',
        'headache, nausea, vomiting',
        'fever, sore throat, cough',
        'stomach pain, diarrhea, nausea',
        'fever, rash, joint pain',
        'cough, wheezing, chest tightness',
        'frequent urination, increased thirst',
        'fatigue, weight loss, increased hunger',
        'fever, chills, sweating',
        'headache, sensitivity to light, stiff neck',
        'chest pain, irregular heartbeat',
        'shortness of breath, fatigue, swelling',
        'abdominal pain, bloating, constipation',
        'fever, cough, difficulty breathing',
        'skin rash, itching, redness',
        'joint pain, stiffness, swelling',
        'back pain, numbness, tingling',
        'dizziness, fainting, weakness',
        'fever, body ache, runny nose',
        'sore throat, difficulty swallowing',
        'nausea, vomiting, loss of appetite',
        'frequent headaches, blurred vision',
        'muscle pain, weakness, fatigue',
        'fever, cough, chest pain, fatigue',
        'headache, fever, body pain, nausea',
        'stomach pain, vomiting, diarrhea',
        'chest pain, sweating, nausea',
        'cough, fever, shortness of breath',
        'headache, dizziness, confusion',
        'joint pain, fever, rash',
        'abdominal pain, fever, vomiting',
        'back pain, fever, chills',
        'cough, wheezing, shortness of breath',
        'fever, sore throat, body ache',
        'chest tightness, cough, mucus',
        'stomach cramps, diarrhea, fever',
        'headache, neck pain, fever',
        'fatigue, weight gain, cold intolerance',
        'fever, headache, muscle pain, rash',
        'cough, fever, night sweats',
        'chest pain, cough, fever',
        'abdominal pain, nausea, fever',
        'joint pain, swelling, redness',
        'fever, chills, body ache, cough',
        'headache, vomiting, sensitivity to light',
        'shortness of breath, chest pain, cough',
        'stomach pain, bloating, gas',
        'fever, rash, sore throat'
    ],
    'disease': [
        'Flu', 'Common Cold', 'Heart Disease', 'Migraine', 'Flu',
        'Gastroenteritis', 'Dengue', 'Asthma', 'Diabetes', 'Diabetes',
        'Malaria', 'Meningitis', 'Heart Disease', 'Heart Failure', 'IBS',
        'Pneumonia', 'Allergic Reaction', 'Arthritis', 'Sciatica', 'Anemia',
        'Flu', 'Tonsillitis', 'Food Poisoning', 'Hypertension', 'Fibromyalgia',
        'Pneumonia', 'Flu', 'Gastroenteritis', 'Heart Attack', 'COVID-19',
        'Stroke', 'Dengue', 'Appendicitis', 'Kidney Infection', 'Asthma',
        'Flu', 'Bronchitis', 'Gastroenteritis', 'Meningitis', 'Hypothyroidism',
        'Dengue', 'Tuberculosis', 'Pneumonia', 'Appendicitis', 'Arthritis',
        'Flu', 'Migraine', 'Pulmonary Embolism', 'IBS', 'Dengue'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

print("Creating disease prediction model...")
print(f"Dataset size: {len(df)} samples")

# Create symptom features
from sklearn.feature_extraction.text import TfidfVectorizer

# Vectorize symptoms
vectorizer = TfidfVectorizer(max_features=100)
X = vectorizer.fit_transform(df['symptoms'])

# Encode diseases
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['disease'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save model, vectorizer, and label encoder
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("\n✅ Model saved successfully!")
print("Files created:")
print("  - model.pkl (Random Forest model)")
print("  - vectorizer.pkl (TF-IDF vectorizer)")
print("  - label_encoder.pkl (Label encoder)")

# Test prediction
test_symptoms = "fever, cough, fatigue"
test_vector = vectorizer.transform([test_symptoms])
prediction = model.predict(test_vector)
predicted_disease = label_encoder.inverse_transform(prediction)[0]
confidence = model.predict_proba(test_vector).max() * 100

print(f"\n🧪 Test Prediction:")
print(f"Symptoms: {test_symptoms}")
print(f"Predicted Disease: {predicted_disease}")
print(f"Confidence: {confidence:.2f}%")

# Show disease information
disease_info = {
    'Flu': {
        'description': 'Influenza is a viral infection that attacks your respiratory system.',
        'precautions': ['Rest', 'Stay hydrated', 'Take fever reducers', 'Avoid contact with others'],
        'medications': ['Paracetamol', 'Ibuprofen', 'Antiviral drugs (if prescribed)'],
        'diet': ['Warm fluids', 'Chicken soup', 'Fruits rich in Vitamin C', 'Honey'],
        'workout': ['Complete rest', 'Light walking after recovery', 'Avoid strenuous exercise']
    },
    'Common Cold': {
        'description': 'A viral infection of your nose and throat (upper respiratory tract).',
        'precautions': ['Rest', 'Stay hydrated', 'Gargle with salt water', 'Use humidifier'],
        'medications': ['Decongestants', 'Pain relievers', 'Cough syrup'],
        'diet': ['Warm liquids', 'Vitamin C rich foods', 'Ginger tea', 'Honey'],
        'workout': ['Rest', 'Light activities only', 'Resume exercise after recovery']
    },
    'COVID-19': {
        'description': 'Coronavirus disease caused by SARS-CoV-2 virus.',
        'precautions': ['Isolate', 'Wear mask', 'Monitor oxygen levels', 'Seek medical help if severe'],
        'medications': ['Paracetamol', 'Vitamin supplements', 'Consult doctor for specific treatment'],
        'diet': ['Protein-rich foods', 'Fruits and vegetables', 'Stay hydrated', 'Zinc supplements'],
        'workout': ['Complete rest', 'Breathing exercises', 'Gradual return to activity']
    },
    'Pneumonia': {
        'description': 'Infection that inflames air sacs in one or both lungs.',
        'precautions': ['Take prescribed antibiotics', 'Rest', 'Stay hydrated', 'Monitor breathing'],
        'medications': ['Antibiotics', 'Fever reducers', 'Cough medicine'],
        'diet': ['Protein-rich foods', 'Fluids', 'Fruits and vegetables', 'Avoid dairy initially'],
        'workout': ['Complete rest', 'Breathing exercises', 'Gradual increase in activity']
    },
    'Diabetes': {
        'description': 'Chronic condition affecting how your body processes blood sugar.',
        'precautions': ['Monitor blood sugar', 'Take medications regularly', 'Regular check-ups', 'Foot care'],
        'medications': ['Insulin', 'Metformin', 'As prescribed by doctor'],
        'diet': ['Low sugar', 'High fiber', 'Whole grains', 'Vegetables', 'Lean proteins'],
        'workout': ['Regular exercise', 'Walking', 'Swimming', 'Yoga', '30 mins daily']
    },
    'Heart Disease': {
        'description': 'Conditions affecting the heart and blood vessels.',
        'precautions': ['Take medications regularly', 'Monitor blood pressure', 'Reduce stress', 'Regular check-ups'],
        'medications': ['As prescribed by cardiologist', 'Blood thinners', 'Beta blockers'],
        'diet': ['Low sodium', 'Low fat', 'Fruits and vegetables', 'Whole grains', 'Fish'],
        'workout': ['Moderate exercise', 'Walking', 'Swimming', 'Avoid heavy lifting']
    },
    'Asthma': {
        'description': 'Chronic condition causing airways to narrow and swell.',
        'precautions': ['Avoid triggers', 'Use inhaler as prescribed', 'Monitor symptoms', 'Keep rescue inhaler handy'],
        'medications': ['Inhalers', 'Bronchodilators', 'Corticosteroids'],
        'diet': ['Avoid food allergens', 'Omega-3 rich foods', 'Fruits and vegetables'],
        'workout': ['Warm up properly', 'Swimming', 'Walking', 'Avoid cold air exercise']
    },
    'Migraine': {
        'description': 'Severe headache with throbbing pain, usually on one side.',
        'precautions': ['Identify triggers', 'Maintain sleep schedule', 'Reduce stress', 'Stay hydrated'],
        'medications': ['Pain relievers', 'Triptans', 'Anti-nausea drugs'],
        'diet': ['Regular meals', 'Avoid trigger foods', 'Stay hydrated', 'Magnesium-rich foods'],
        'workout': ['Regular exercise', 'Yoga', 'Avoid intense workouts during attack']
    }
}

# Save disease information
with open('disease_info.pkl', 'wb') as f:
    pickle.dump(disease_info, f)

print("\n✅ Disease information database saved!")
print("\nModel training complete! Ready to use in the application.")
