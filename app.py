import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("pcos_diagnosis_pipeline.pkl")

# Title and introduction
st.title("🌸 PCOS Diagnosis Tool")

# Side menu for selecting user type
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.title("User Type")
user_type = st.sidebar.selectbox("I am a:", ["Patient", "Healthcare Provider"])

if user_type == "Patient":
    st.image("Young Person Engaging With Telemedicine App In Healthcare Setting.png", use_container_width=True)
    st.markdown("""
    Welcome to the **PCOS Diagnosis Tool**! 
    This tool is designed for both patients and healthcare professionals to assess the likelihood of PCOS.
    Please answer the questions carefully. Your privacy is respected, and the data is not saved.
    """)
    
    st.sidebar.image("hal-gatewood-OgvqXGL7XO4-unsplash.jpg", use_container_width=True)
    
    # Section 1: General Information
    st.header("📋 General Information")
    patient_name = st.text_input("What is your name?")
    birth_control = st.radio(
        "Are you currently receiving birth control pills or injections?", 
        ["Yes", "No"], 
        index=1
    )
    ovaries_removed = st.radio(
        "Have you had both ovaries or uterus removed?", 
        ["Yes", "No"], 
        index=1
    )
    additional_notes = st.text_area("Any additional information you'd like to share? (Optional)")

    # Section 2: Ovulatory Dysfunction
    st.header("📅 Ovulatory Dysfunction")
    menstrual_cycle_length = st.selectbox(
        "How long is your average menstrual cycle?",
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
        "Do you have a tendency to grow dark, coarse hair?",
        ["Yes", "No"], 
        index=1
    )

    # Section 4: Ultrasound Findings
    st.header("🔬 Ultrasound Findings")
    st.write("If you have undergone an ultrasound, please provide the following details:")

    follicle_count = st.number_input(
        "Do you know the number of follicles seen in your ultrasound? (Enter a number or leave blank if unknown)",
        min_value=0, step=1, format="%d", help="Typically, a follicle count of 12 or more may indicate PCOS."
    )
    ovarian_volume = st.number_input(
        "What is the volume of your ovaries according to the report? (in cm³)",
        min_value=0.0, step=0.1, format="%.1f",
        help="Ovarian volume greater than 10 cm³ is often considered a feature of PCOS."
    )
    stroma_endometrial_status = st.radio(
        "Was there mention of increased stroma or abnormal endometrial thickness?",
        options=["Yes", "No", "Not Sure"],
        help="Increased stroma or irregular endometrial thickness can be an indication of hormonal imbalance."
    )
    ultrasound_findings = st.multiselect(
        "Select all findings mentioned in your ultrasound report:",
        options=[
            "A big womb", "A tilted womb", "Fibroids", "Polyps",
            "Swollen tubes", "Ovarian cysts", "Endometriosis",
            "Adenomyosis", "Adhesions", "Thickening of the lining of the womb", "None of the above"
        ],
        help="Select the findings listed in your ultrasound report. Choose 'None of the above' if no findings were reported."
    )

    # Section 5: Obesity
    st.header("⚖️ Obesity")
    st.write("Would you like to calculate your BMI?")
    weight = st.number_input("Enter your weight (kg):", min_value=20.0, max_value=200.0, step=0.1)
    height = st.number_input("Enter your height (cm):", min_value=100.0, max_value=250.0, step=0.1)
    if weight and height:
        bmi = round(weight / ((height / 100) ** 2), 2)
        st.write(f"Your calculated BMI is: {bmi}")
    else:
        bmi = None

    # Section 6: Hormonal and Other Measurements
    st.header("🧪 Hormonal and Other Measurements")
    fasting_glucose = st.number_input("What is your fasting glucose level (mg/dL)?")
    fasting_insulin = st.number_input("What is your fasting insulin level (µIU/mL)?")
    lh_fsh_ratio = st.number_input("What is your LH/FSH ratio?")
    amh = st.number_input("What is your AMH (Anti-Müllerian Hormone) level (ng/mL)?")
    dheas = st.number_input("What is your DHEAS (Dehydroepiandrosterone sulfate) level (µg/dL)?")
    prolactin = st.number_input("What is your prolactin level (ng/mL)?")
    tsh = st.number_input("What is your TSH (Thyroid Stimulating Hormone) level (mIU/L)?")
    free_testosterone = st.number_input("What is your free testosterone level (pg/mL)?")
    blood_sugar = st.number_input("What is your random blood sugar level (mg/dL)?")
    score = st.slider("On a scale of 1 to 10, how would you rate your symptom severity?", 1, 10)

    # Predict button
    if st.button("Predict"):
        try:
            # Prepare the input data for the model
            input_data = pd.DataFrame([{
                "Age": None,  # Replace with the appropriate age input
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
            diagnosis = "PCOS Likely" if likelihood > 50 else "PCOS Unlikely"

            # Display the results
            st.success(f"Prediction for {patient_name or 'the patient'}: {diagnosis}")
            st.write(f"PCOS Likelihood: {likelihood:.2f}%")
            if additional_notes:
                st.info(f"Additional Notes Provided: {additional_notes}")
        except ValueError as e:
            st.error(f"An error occurred: {e}. Please ensure all fields are correctly filled.")

elif user_type == "Healthcare Provider":
    st.sidebar.image("doctor.webp", use_container_width=True)
    st.header("🩺 Healthcare Provider Section")
    st.write("This section allows healthcare providers to input patient details and receive a PCOS likelihood assessment. Please fill out the following information carefully.")

    # Section 1: General Information
    st.header("📋 General Information")
    patient_name = st.text_input("Patient's Name")
    patient_age = st.number_input("Patient's Age", min_value=0, step=1, format="%d")
    patient_gender = st.radio("Patient's Gender", ["Female", "Male", "Other"], index=0)
    patient_id = st.text_input("Patient ID")
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
        "Mention of increased stroma or abnormal endometrial thickness?",
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
            diagnosis = "PCOS Likely" if likelihood > 50 else "PCOS Unlikely"

            # Display the results
            st.success(f"Prediction for {patient_name or 'the patient'}: {diagnosis}")
            st.write(f"PCOS Likelihood: {likelihood:.2f}%")
            if additional_notes:
                st.info(f"Additional Notes Provided: {additional_notes}")
        except ValueError as e:
            st.error(f"An error occurred: {e}. Please ensure all fields are correctly filled.")

# Footer note
st.markdown("""
**Disclaimer:** This tool is for informational purposes only and is not a substitute for professional medical advice. Please consult a healthcare provider for a definitive diagnosis.
""")