import re
import streamlit as st
from pathlib import Path
from analyzer import analyze_resume
from resume_builder import build_resume
from pdf_builder import build_resume_pdf
from utils import read_file
from emailer import send_email

st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 ATS Resume Analyzer")

# Session State
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "jd_text" not in st.session_state:
    st.session_state.jd_text = None

if "result" not in st.session_state:
    st.session_state.result = None

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "txt","docx"]
)

# Job Description
jd = st.text_area(
    "Paste Job Description",
    height=200
)

# Email
email = st.text_input(
    "Enter Email Address"
)

# Analyze Button
if st.button("Analyze Resume"):

    if uploaded_file is None:
        st.error("Please upload a resume")
        st.stop()

    if not jd:
        st.error("Please enter Job Description")
        st.stop()

    if email.strip():

        pattern = r"^[^@]+@[^@]+\.[^@]+$"

        if not re.match(pattern, email.strip()):
            st.error("Please enter a valid email address")
            st.stop()

    Path("uploads").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    file_path = f"uploads/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume = read_file(file_path)

    st.session_state.resume_text = resume
    st.session_state.jd_text = jd

    with st.spinner("Analyzing Resume..."):
        result = analyze_resume(resume, jd)

    st.session_state.result = result

if email.strip():

    pattern = r"^[^@]+@[^@]+\.[^@]+$"

    if not re.match(pattern, email.strip()):
        st.error("Please enter a valid email address")
        st.stop()

    Path("uploads").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    file_path = f"uploads/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    resume = read_file(file_path)

    st.session_state.resume_text = resume
    st.session_state.jd_text = jd

    with st.spinner("Analyzing Resume..."):
        result = analyze_resume(resume, jd)

    st.session_state.result = result

# Show Results
if st.session_state.result is not None:

    result = st.session_state.result

    st.success("Analysis Complete")

    st.subheader("ATS Score")
    st.metric("Score", result["final_score"])

    st.subheader("Rating")
    st.write(result["rating"])

    st.subheader("Matched Keywords")
    st.write(result["matched_keywords"])

    st.subheader("Missing Keywords")
    st.write(result["missing_keywords"])

    st.subheader("Suggestions")
    st.write(result["improvements"])

    # Generate Resume Button
    if st.button("Generate ATS Resume"):

        try:

            with st.spinner("Generating Resume..."):

                resume_text = build_resume(
                    st.session_state.resume_text,
                    st.session_state.jd_text
                )

                pdf_path = build_resume_pdf(
                    resume_text,
                    "output/ATS_Resume.pdf"
                )

            st.success("✅ Resume Generated Successfully")

            # Email Send
            if email.strip():

                try:
                    send_email(email.strip(), pdf_path)
                    st.success(f"✅ Resume sent to {email}")

                except Exception as e:
                    st.error(f"❌ Email Error: {str(e)}")

            # Download Button
            with open(pdf_path, "rb") as pdf_file:

                st.download_button(
                    label="📥 Download ATS Resume",
                    data=pdf_file,
                    file_name="ATS_Resume.pdf",
                    mime="application/pdf"
                )
                

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")