import re
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

STOP_WORDS = {
    "the", "and", "to", "of", "in", "a", "for", "on", "with",
    "is", "are", "this", "that", "by", "as", "an", "be",
    "at", "from", "or", "it", "we", "you", "your", "will",
    "into", "use", "using", "their", "our", "they"
}

def extract_keywords(text):
    words = re.findall(r'\w+', text.lower())
    return set([w for w in words if w not in STOP_WORDS and len(w) > 2])


def get_ai_suggestions(resume, jd, missing_keywords, score):

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the resume against the job description and give ONLY 6-8 strong, practical suggestions.

Rules:
- Be specific and personalized
- Do NOT give generic advice
- Focus on missing skills and improvements
- Keep suggestions short and actionable

ATS Score: {score}

Missing Keywords:
{missing_keywords}

Resume:
{resume}

Job Description:
{jd}

Return only bullet points.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.split("\n")


def analyze_resume(resume, jd):

    resume_words = extract_keywords(resume)
    jd_words = extract_keywords(jd)

    if not jd_words:
        return {
            "ats_score": 0,
            "keyword_match_percentage": 0,
            "missing_keywords": [],
            "suggestions": ["Job description is empty"]
        }

    common_words = resume_words & jd_words

    match_percentage = (len(common_words) / len(jd_words)) * 100

    missing_keywords = list(jd_words - resume_words)

    # AI-generated suggestions
    suggestions = get_ai_suggestions(
        resume,
        jd,
        missing_keywords[:10],
        round(match_percentage, 2)
    )

    return {
        "ats_score": round(match_percentage, 2),
        "keyword_match_percentage": round(match_percentage, 2),
        "missing_keywords": missing_keywords[:10],
        "suggestions": suggestions
    }