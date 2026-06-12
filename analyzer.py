import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------
# 1. AI → Only suggestions
# ----------------------------
def get_ai_suggestions(missing_keywords):
    prompt = f"""
You are an ATS Resume Expert.

Missing Keywords:
{missing_keywords}

Give 6 short ATS improvement suggestions.
Return bullet points only.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return [
            x.strip("-• ").strip()
            for x in response.choices[0].message.content.split("\n")
            if x.strip()
        ]

    except:
        return []


# ----------------------------
# 2. MAIN ATS ENGINE
# ----------------------------
def analyze_resume(resume, jd):

    # -------- manual keyword extraction (IMPORTANT) --------
    jd_keywords = list(set([
        word.strip()
        for word in jd.replace(",", " ").split()
        if len(word) > 2
    ]))

    resume_text = resume.lower()

    matched_keywords = []
    missing_keywords = []

    for keyword in jd_keywords:
        if keyword.lower() in resume_text:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    # -------- SCORE CALCULATION (FIXED) --------
    keyword_score = int((len(matched_keywords) / len(jd_keywords)) * 50) if jd_keywords else 0

    title_score = 15 if "python" in resume_text else 5

    format_score = 15 if "experience" in resume_text.lower() else 10

    experience_score = 10 if len(resume.split()) > 100 else 5

    penalty_score = 0

    final_score = keyword_score + title_score + format_score + experience_score - penalty_score

    if final_score >= 90:
        rating = "EXCELLENT MATCH"
    elif final_score >= 75:
        rating = "STRONG MATCH"
    elif final_score >= 60:
        rating = "GOOD MATCH"
    elif final_score >= 40:
        rating = "FAIR MATCH"
    else:
        rating = "POOR MATCH"

    suggestions = get_ai_suggestions(missing_keywords[:10])

    return {
        "keyword_score": keyword_score,
        "title_score": title_score,
        "format_score": format_score,
        "experience_score": experience_score,
        "penalty_score": penalty_score,
        "final_score": final_score,
        "rating": rating,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "improvements": suggestions
    }