import os
from dotenv import load_dotenv
from groq import Groq

def build_resume(resume, jd):

    # Load environment variables
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Check your .env file")

    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert AI Resume Writer and ATS optimization specialist.

Your task is to rewrite the resume into a HIGHLY PROFESSIONAL, ATS-OPTIMIZED resume.

🎯 Goals:
- Make the resume clear, structured, and easy for recruiters to read
- Improve grammar, formatting, and sentence flow
- Optimize for ATS keyword matching with the job description
- Make the resume impactful and job-ready

⚠️ Strict Rules:
- Do NOT invent fake experience, skills, or projects
- Do NOT exaggerate facts
- Only improve and restructure existing content

✨ What you SHOULD do:
- Rewrite bullet points using strong action verbs
- Improve clarity and readability
- Align resume language with job description keywords
- Make skills section clean and relevant
- Improve professional tone

📌 Job Description:
{jd}

📄 Original Resume:
{resume}

🧠 Output Format:
Return a clean ATS-friendly resume with:
- Professional Summary
- Skills
- Experience (if available)
- Projects (if available)
- Education
- Certifications (if available)

Make it recruiter-friendly and ATS-optimized.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content