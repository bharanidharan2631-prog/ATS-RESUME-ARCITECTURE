from pathlib import Path
from utils import read_file
from analyzer import analyze_resume
from resume_builder import build_resume

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

result = analyze_resume(resume, jd)

print("\n" + "=" * 40)
print("RESULTS")
print("=" * 40)

print("\nATS SCORE:", result.get("ats_score", "N/A"))
print("KEYWORD MATCH:", result.get("keyword_match_percentage", "N/A"), "%")

print("\nMISSING KEYWORDS")
for item in result.get("missing_keywords", []):
    print("-", item)

print("\nSUGGESTIONS")
for item in result.get("suggestions", []):
    print("-", item)

choice = input("\nGenerate ATS Resume? (y/n): ")

if choice.lower() == "y":
    Path("output").mkdir(exist_ok=True)

    resume_text = build_resume(resume, jd)

    with open("output/ats_resume.txt", "w", encoding="utf-8") as f:
        f.write(resume_text)

    print("\nATS Resume saved to output/ats_resume.txt")