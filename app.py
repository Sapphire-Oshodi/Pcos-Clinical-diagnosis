import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib

def calculate_risk(answers):
    criteria_met = sum(answers[:3]) >= 1, sum(answers[3:6]) >= 1, sum(answers[6:8]) >= 1
    criteria_count = sum(criteria_met)
    
    if criteria_count == 0:
        return "Low Risk", "#4CAF50"
    elif criteria_count == 1:
        return "Moderate Risk", "#FF9800"
    else:
        return "High Risk", "#F44336"

# Set page config
st.set_page_config(page_title="PCOS Self-Assessment", page_icon="🌸", layout="centered")

# Load the trained model
model = joblib.load("pcos_diagnosis_pipeline.pkl")

# Custom CSS for styling
st.markdown("""
    <style>
        body {background-color: #f5f5f5; font-family: Arial, sans-serif;}
        .stButton>button {background-color: #6200ea; color: white; padding: 10px 20px; font-size: 18px; border-radius: 8px;}
        .stRadio > label {font-size: 18px;}
        .result-box {border-radius: 10px; padding: 20px; text-align: center; font-size: 20px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# Side menu for selecting user type
st.sidebar.image("logo.png")
st.sidebar.title("User Type")
user_type = st.sidebar.selectbox("I am a:", ["Patient", "Healthcare Provider"])

if user_type == "Patient":
    st.header("🌸 PCOS Self-Assessment Quiz 🌸")
    st.image("Young Person Engaging With Telemedicine App In Healthcare Setting.png")
    st.markdown("""
    Welcome to the **PCOS Symptoms and Diagnosis Tool**! 
    This tool is designed for both patients and healthcare professionals to assess the likelihood of PCOS.
    Please answer the questions carefully. Your privacy is respected, and the data is not saved.
    """)
    
    st.sidebar.image("hal-gatewood-OgvqXGL7XO4-unsplash.jpg")


    questions = [
        # Ovulatory dysfunction
        ("Do you have irregular or missed periods (fewer than 9 per year)?", "Irregular periods are a common sign of ovulatory dysfunction."),
        ("Have you gone more than 35 days without a period?", "Long cycles may indicate hormonal imbalances."),
        ("Do you often experience very light or very heavy periods?", "Extreme variations in period flow can be a sign of ovulatory issues."),
        # Hyperandrogenism
        ("Do you have excessive hair growth on your face, chest, or back?", "Hirsutism is a key indicator of high androgen levels."),
        ("Have you noticed persistent acne or very oily skin?", "High androgen levels can cause persistent acne and oiliness."),
        ("Do you experience significant hair thinning or hair loss on your scalp?", "Male-pattern baldness or thinning hair may suggest hormonal imbalance."),
        # Polycystic Ovaries
        ("Have you been diagnosed with polycystic ovaries on an ultrasound?", "Polycystic ovaries are a diagnostic factor for PCOS."),
        ("Have you ever been diagnosed with ovarian cysts?", "Ovarian cysts can contribute to PCOS symptoms."),
        # Additional symptoms
        ("Do you have unexplained weight gain or difficulty losing weight?", "Insulin resistance can lead to weight gain in PCOS."),
        ("Do you feel unusually fatigued or low on energy?", "Hormonal imbalances can cause fatigue."),
        ("Do you have darkened patches of skin (e.g., on your neck, armpits, or groin)?", "Acanthosis nigricans is often linked to insulin resistance.")
    ]

    answers = []
    st.markdown("### Answer the following questions")
    with st.form("pcos_quiz"):
        for question, explanation in questions:
            response = st.radio(f"**{question}**\n*{explanation}*", ["No", "Yes"], index=0, horizontal=True)
            answers.append(1 if response == "Yes" else 0)
        submit = st.form_submit_button("Submit Assessment")

    if submit:
        risk_level, color = calculate_risk(answers)
        st.markdown(f"""
            <div class='result-box' style='background-color:{color}; color: white;'>
                Your Risk Level: {risk_level}
            </div>
        """, unsafe_allow_html=True)
        st.write("The Rotterdam Criteria require at least 2 out of 3 factors (Irregular periods, Hyperandrogenism, Polycystic ovaries) to diagnose PCOS. If you are at moderate or high risk, consider consulting a healthcare professional for further evaluation.")

elif user_type == "Healthcare Provider":
    st.sidebar.image("doctor.webp")
    st.title("🌸 PCOS Diagnosis Tool")
    st.header("🩺 Healthcare Provider Section")
    st.write("This section allows healthcare providers to input patient details and receive a PCOS likelihood assessment. Please fill out the following information carefully.")

    # Section 1: General Information
    st.header("📋 General Information")
    patient_name = st.text_input("Patient's Name")
    patient_age = st.slider("Patient's Age", min_value=10, max_value=90, value=25, step=1)
    additional_notes = st.text_area("Additional Notes (Optional)")

    # Section 2: Ovulatory Dysfunction
    st.header("📅 Ovulatory Dysfunction")
    menstrual_cycle_length = st.selectbox(
        "Average Menstrual Cycle Length",
        [
            "Less than 25 days", 
            "25–34 days", 
            "35–60 days", 
            "More than 60 days", 
            "Totally variable (changes frequently)"
        ]
    )

    # Section 3: Hyperandrogenism
    st.header("🌿 Hyperandrogenism")
    excess_hair_growth = st.radio(
        "Tendency to grow dark, coarse hair?",
        ["Yes", "No"], 
        index=1
    )

    # Section 4: Ultrasound Findings
    st.header("🔬 Ultrasound Findings")
    st.write("If the patient has undergone an ultrasound, please provide the following details:")

    follicle_count = st.number_input(
        "Number of follicles seen in ultrasound", min_value=0, step=1, format="%d"
    )
    ovarian_volume = st.number_input(
        "Volume of ovaries (in cm³)", min_value=0.0, step=0.1, format="%.1f"
    )
    stroma_endometrial_status = st.radio(
        "Was there a mention of increased stroma or abnormal endometrial thickness?",
        options=["Yes", "No", "Not Sure"]
    )
    ultrasound_findings = st.multiselect(
        "Findings mentioned in ultrasound report:",
        options=[
            "A big womb", "A tilted womb", "Fibroids", "Polyps",
            "Swollen tubes", "Ovarian cysts", "Endometriosis",
            "Adenomyosis", "Adhesions", "Thickening of the lining of the womb", "None of the above"
        ]
    )

    # Section 5: Obesity
    st.header("⚖️ Obesity")
    st.write("Calculate BMI:")
    weight = st.number_input("Weight (kg):", min_value=20.0, max_value=200.0, step=0.1)
    height = st.number_input("Height (cm):", min_value=100.0, max_value=250.0, step=0.1)
    if weight and height:
        bmi = round(weight / ((height / 100) ** 2), 2)
        st.write(f"Calculated BMI: {bmi}")
    else:
        bmi = None

    # Section 6: Hormonal and Other Measurements
    st.header("🧪 Hormonal and Other Measurements")
    fasting_glucose = st.number_input("Fasting Glucose Level (mg/dL)")
    fasting_insulin = st.number_input("Fasting Insulin Level (µIU/mL)")
    lh_fsh_ratio = st.number_input("LH/FSH Ratio")
    amh = st.number_input("AMH (Anti-Müllerian Hormone) Level (ng/mL)")
    dheas = st.number_input("DHEAS (Dehydroepiandrosterone sulfate) Level (µg/dL)")
    prolactin = st.number_input("Prolactin Level (ng/mL)")
    tsh = st.number_input("TSH (Thyroid Stimulating Hormone) Level (mIU/L)")
    free_testosterone = st.number_input("Free Testosterone Level (pg/mL)")
    blood_sugar = st.number_input("Random Blood Sugar Level (mg/dL)")
    score = st.slider("Symptom Severity (1 to 10)", 1, 10)

    # Predict button
    if st.button("Predict PCOS Likelihood"):
        try:
            # Prepare the input data for the model
            input_data = pd.DataFrame([{
                "Age": patient_age,
                "BMI": bmi,
                "FastingGlucose": fasting_glucose,
                "FastingInsulin": fasting_insulin,
                "LH_FSH_Ratio": lh_fsh_ratio,
                "AMH": amh,
                "DHEAS": dheas,
                "Prolactin": prolactin,
                "TSH": tsh,
                "FreeTestosterone": free_testosterone,
                "BloodSugar": blood_sugar,
                "Score": score
            }])
            
            # Make the prediction
            probabilities = model.predict_proba(input_data)[0]
            likelihood = probabilities[1] * 100

            # Display the results
            if likelihood > 50:
                diagnosis = "PCOS Likely"
                st.success(f"Prediction for {patient_name or 'the patient'}: {diagnosis}")
                st.write(f"PCOS Likelihood: {likelihood:.2f}%")
                st.info("Based on the provided information, it is likely that the patient has PCOS. Please consult with a healthcare provider for further evaluation and confirmation.")
            else:
                diagnosis = "PCOS Unlikely"
                st.success(f"Prediction for {patient_name or 'the patient'}: {diagnosis}")
                st.write(f"PCOS Likelihood: {likelihood:.2f}%")
                st.info("Based on the provided information, it is unlikely that the patient has PCOS. Please consult with a healthcare provider for further evaluation if symptoms persist.")
            
            if additional_notes:
                st.info(f"Additional Notes Provided: {additional_notes}")
        except ValueError as e:
            st.error(f"An error occurred: {e}. Please ensure all fields are correctly filled.")

# Footer note
st.markdown("""
**Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice. Please consult a healthcare provider for a definitive diagnosis.
""")
