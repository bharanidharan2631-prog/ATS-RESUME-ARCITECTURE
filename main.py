from pathlib import Path
from utils import read_file
from analyzer import analyze_resume
from resume_builder import build_resume
from pdf_builder import build_resume_pdf

print("=" * 60)
print("ATS Resume Analyzer")
print("=" * 60)

resume_path = input("Resume file path: ").strip()

if not Path(resume_path).exists():
    print("File not found")
    exit()

resume = read_file(resume_path)

print("\nPaste Job Description (Press Enter twice)\n")

lines = []
blank = 0

while True:
    line = input()

    if line == "":
        blank += 1

        if blank == 2:
            break
    else:
        blank = 0

    lines.append(line)

jd = "\n".join(lines).strip()

# ATS Analysis
result = analyze_resume(resume, jd)
print("\n========================================")
print("ATS ANALYSIS REPORT")
print("========================================")

print(f"\nKeyword Match Score   : {result.get('keyword_score',0)}/50")
print(f"Job Title Match Score : {result.get('title_score',0)}/20")
print(f"Formatting Score      : {result.get('format_score',0)}/15")
print(f"Experience Score      : {result.get('experience_score',0)}/10")
print(f"Penalty Score         : {result.get('penalty_score',0)}/5")

print("\n----------------------------------------")
print(f"FINAL ATS SCORE       : {result.get('final_score',0)}/100")
print("----------------------------------------")

print(f"\nATS Rating            : {result.get('rating','N/A')}")

print("\nMATCHED KEYWORDS")
for item in result.get("matched_keywords", []):
    print("✓", item)

print("\nMISSING KEYWORDS")
for item in result.get("missing_keywords", []):
    print("-", item)

print("\nIMPROVEMENTS")
for item in result.get("improvements", []):
    print("-", item)