import streamlit as st
import fitz  # PyMuPDF
import re

# ------------ Required Skills List -------------
REQUIRED_SKILLS = ["python", "java", "sql", "html", "css", "machine learning", "nlp"]

# ------------ Extract text from PDF resume -------------
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ------------ Extract skills from text -------------
def extract_skills(text):
    skill_keywords = [
        "python", "java", "c++", "html", "css", "javascript",
        "sql", "mysql", "mongodb", "react", "node", "django",
        "machine learning", "deep learning", "nlp", "data science",
        "pandas", "numpy", "opencv", "git", "github", "flask"
    ]
    text = text.lower()
    found_skills = [skill for skill in skill_keywords if skill in text]
    return list(set(found_skills))

# ------------ Extract experience from text -------------
def extract_experience(text):
    experience_patterns = [
        r"\d+\s+years?\s+of\s+experience",
        r"experience\s+of\s+\d+\s+years?",
        r"\d+\s+(?:months?|years?)\s+(?:of\s+)?experience",
        r"\d+\s+(?:month|months)\s+internship",
        r"\d+\s+(?:month|months)\s+training",
        r"intern(?:ship)?\s+(?:at|with)\s+[\w\s&]+",
        r"worked\s+(?:at|with)\s+[\w\s&]+",
        r"\d{4}\s*[-–]\s*\d{4}",
        r"\d+\s+(?:months?|years?)\s+in\s+[\w\s]+",
    ]
    matches = []
    for pattern in experience_patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        matches.extend(found)
    return list(set(matches))

# ------------ Calculate skill match -------------
def calculate_skill_match(extracted_skills, required_skills):
    extracted = set(skill.lower() for skill in extracted_skills)
    required = set(skill.lower() for skill in required_skills)
    matched = extracted.intersection(required)
    match_score = (len(matched) / len(required)) * 100
    return matched, round(match_score, 2)

# ------------ Streamlit UI -------------
st.set_page_config(page_title="Resume Screener", layout="centered")
st.title("📄 Resume Screener using NLP")
st.write("Upload a PDF resume to extract skills and experience.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

        skills = extract_skills(resume_text)
        experience = extract_experience(resume_text)

        st.subheader("🧠 Extracted Skills")
        st.write(", ".join(skills) if skills else "No skills found.")

        st.subheader("💼 Extracted Experience")
        st.write(", ".join(experience) if experience else "No experience found.")

        matched_skills, score = calculate_skill_match(skills, REQUIRED_SKILLS)

        st.subheader("🎯 Skill Match Result")
        st.write(f"Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}")
        st.write(f"✅ Skill Match Score: **{score}%**")

        if score >= 70:
            st.success("Great Match!")
        elif score >= 40:
            st.warning("Average Match – can improve.")
        else:
            st.error("Poor Match – missing important skills.")





