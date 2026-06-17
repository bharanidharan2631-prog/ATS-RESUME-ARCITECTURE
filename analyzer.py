import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------
# AI Suggestions
# ----------------------------
def get_ai_suggestions(missing_keywords):

    if not missing_keywords:
        return ["Resume is well aligned with the job description."]

    prompt = f"""
You are an ATS Resume Expert.

Missing Keywords:
{', '.join(missing_keywords)}

Generate EXACTLY 8 ATS resume improvement suggestions.

Rules:
- One line per suggestion
- Maximum 12 words per suggestion
- Focus only on missing keywords
- No examples
- No explanations
- No quotation marks
- No numbering
- Professional ATS language

Return ONLY 8 bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        suggestions = [
            x.strip("-• ").strip()
            for x in response.choices[0].message.content.split("\n")
            if x.strip()
        ]

        return suggestions[:8]

    except Exception:
        return []


# ----------------------------
# Keyword Extraction
# ----------------------------
def extract_keywords(text):

    stop_words = {

        "a","an","the",
        "and","or","but",
        "for","with","without",
        "into","from","of","to",
        "in","on","at","by",

        "you","your","yours",
        "we","our","ours",
        "they","their","them",

        "is","am","are","was","were",
        "be","been","being",
        "have","has","had",
        "do","does","did",
        "will","would","shall",
        "should","can","could",
        "may","might","must",

        "job","role","position",
        "candidate","applicant",
        "required","preferred",

        "responsibility",
        "responsibilities",
        "qualification",
        "qualifications",

        "experience",
        "experiences",
        "year",
        "years",

        "strong",
        "good",
        "excellent",

        "knowledge",
        "ability",
        "abilities",

        "skill",
        "skills",

        "team",
        "teams",

        "company",
        "organization",
        "business",

        "environment",
        "opportunity",

        "using",
        "used",
        "user",
        "users",

        "support",
        "supporting",
        "supported",

        "develop",
        "developer",
        "development",

        "design",
        "designed",

        "build",
        "building",
        "built",

        "create",
        "created",
        "creating",

        "work",
        "worked",
        "working"
    }

    words = re.findall(
        r"\b[a-zA-Z0-9+#.]+\b",
        text.lower()
    )

    keywords = []

    for word in words:

        if len(word) > 2 and word not in stop_words:
            keywords.append(word)

    return sorted(list(set(keywords)))


# ----------------------------
# MAIN ATS ENGINE
# ----------------------------
def analyze_resume(resume, jd):

    resume_text = resume.lower()
    jd_text = jd.lower()

    # ----------------------------
    # Keyword Matching (60)
    # ----------------------------

    jd_keywords = extract_keywords(jd)

    matched_keywords = []
    missing_keywords = []

    for keyword in jd_keywords:

        if keyword in resume_text:
            matched_keywords.append(keyword)

        else:
            missing_keywords.append(keyword)

    keyword_score = (
        int(
            (len(matched_keywords) / len(jd_keywords)) * 60
        )
        if jd_keywords
        else 0
    )

    # ----------------------------
    # Job Title Match (10)
    # ----------------------------

    title_score = 0

    common_titles = [
        "python developer",
        "java developer",
        "software engineer",
        "software developer",
        "backend developer",
        "frontend developer",
        "full stack developer",
        "data analyst",
        "data scientist",
        "devops engineer",
        "machine learning engineer"
    ]

    detected_title = None

    for title in common_titles:

        if title in jd_text:
            detected_title = title
            break

    if detected_title and detected_title in resume_text:
        title_score = 10

    elif detected_title:
        title_score = 5

    # ----------------------------
    # Skills Section (10)
    # ----------------------------

    skills_score = 0

    if "skills" in resume_text:
        skills_score += 5

    if len(matched_keywords) >= 5:
        skills_score += 5

    skills_score = min(skills_score, 10)

    # ----------------------------
    # Experience Section (5)
    # ----------------------------

    experience_score = 5 if any(
        x in resume_text
        for x in [
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "employment history"
        ]
    ) else 0

    # ----------------------------
    # Projects Section (5)
    # ----------------------------

    project_score = 5 if any(
        x in resume_text
        for x in [
            "project",
            "projects",
            "academic projects",
            "personal projects"
        ]
    ) else 0

    # ----------------------------
    # Education Section (5)
    # ----------------------------

    education_score = 5 if any(
        x in resume_text
        for x in [
            "education",
            "degree",
            "college",
            "university"
        ]
    ) else 0

    # ----------------------------
    # Formatting Score (5)
    # ----------------------------

    sections_found = 0

    if "skills" in resume_text:
        sections_found += 1

    if experience_score > 0:
        sections_found += 1

    if education_score > 0:
        sections_found += 1

    if project_score > 0:
        sections_found += 1

    format_score = min(5, sections_found)

    # ----------------------------
    # Penalty Score
    # ----------------------------

    penalty_score = 0

    if len(missing_keywords) > len(matched_keywords):
        penalty_score += 5

    if len(resume.split()) < 120:
        penalty_score += 5

    # ----------------------------
    # Final ATS Score
    # ----------------------------

    final_score = (
        keyword_score
        + title_score
        + skills_score
        + experience_score
        + project_score
        + education_score
        + format_score
        - penalty_score
    )

    final_score = max(
        0,
        min(final_score, 100)
    )

    # ----------------------------
    # Rating
    # ----------------------------

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

    suggestions = get_ai_suggestions(
        missing_keywords[:10]
    )

    return {
        "keyword_score": keyword_score,
        "title_score": title_score,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "project_score": project_score,
        "education_score": education_score,
        "format_score": format_score,
        "penalty_score": penalty_score,
        "final_score": final_score,
        "rating": rating,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "improvements": suggestions
    }
