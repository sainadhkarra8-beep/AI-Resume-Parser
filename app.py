import streamlit as st
import pdfplumber
import spacy
import re

# Load NLP model
nlp = spacy.load("en_core_web_sm")

st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Parser")
st.write("Upload a resume and extract important information using AI/NLP.")

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)

if uploaded_file is not None:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    if text.strip():

        doc = nlp(text)

        # Extract email
        email = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )

        # Extract phone number
        phone_matches = re.findall(
            r'(?:(?:\+|00)91[\s.-]*)?[6-9]\d{4}[\s.-]?\d{5}',
            text
        )

        phone = phone_matches[0] if phone_matches else None

        # Extract entities
        names = [
            ent.text for ent in doc.ents
            if ent.label_ == "PERSON"
        ]

        organizations = [
            ent.text for ent in doc.ents
            if ent.label_ == "ORG"
        ]

        # Extract skills
        skills_list = [
            "Python", "Java", "C++", "SQL", "HTML", "CSS",
            "JavaScript", "Machine Learning", "Deep Learning",
            "NLP", "Artificial Intelligence", "Git",
            "Streamlit", "TensorFlow", "PyTorch"
        ]

        found_skills = []

        for skill in skills_list:
            if skill.lower() in text.lower():
                found_skills.append(skill)

        st.success("Resume processed successfully!")

        st.subheader("📌 Extracted Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("### 👤 Name")
            st.write(names[0] if names else "Not found")

            st.write("### 📧 Email")
            st.write(email[0] if email else "Not found")

            st.write("### 🛠️ Skills")
            if found_skills:
                for skill in found_skills:
                    st.write(f"- {skill}")
            else:
                st.write("No skills found")

        with col2:
            st.write("### 📱 Phone")
            st.write(phone if phone else "Not found")

            st.write("### 🏢 Organizations")
            if organizations:
                for org in organizations:
                    st.write(f"- {org}")
            else:
                st.write("Not found")

        st.subheader("📄 Resume Text")

        with st.expander("View extracted resume text"):
            st.write(text)

    else:
        st.error("Could not extract text from this resume.")