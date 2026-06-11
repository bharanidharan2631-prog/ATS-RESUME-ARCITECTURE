import os
from dotenv import load_dotenv
from groq import Groq

def build_resume(resume, jd):

    # Load .env every time safely
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("❌ GROQ_API_KEY not found. Check your .env file")

    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert ATS Resume Writer.

Rewrite the resume to maximize ATS compatibility.

Rules:
- Do not invent experience
- Do not invent projects
- Do not invent certifications
- Do not invent skills

You may:
- Improve formatting
- Improve summary
- Improve bullet points
- Improve ATS keyword placement

Job Description:
{jd}

Resume:
{resume}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content