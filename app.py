from flask import Flask, render_template, request, jsonify
from analyzer import analyze_resume
from resume_builder import build_resume
from pdf_builder import build_resume_pdf
from emailer import send_email
from utils import read_file
from pathlib import Path

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files["resume"]
    jd = request.form["jd"]
    email = request.form["email"]

    Path("uploads").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    file_path = f"uploads/{resume_file.filename}"
    resume_file.save(file_path)

    resume = read_file(file_path)

    # ATS ANALYSIS
    result = analyze_resume(resume, jd)

    # AI RESUME REBUILD
    resume_text = build_resume(resume, jd)

    # PDF GENERATION
    pdf_path = build_resume_pdf(resume_text, "output/ats_resume.pdf")

    # EMAIL SEND
    send_email(email, pdf_path)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)