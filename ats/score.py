from datetime import datetime
from ats.skill_match import compute_skill_match
# Fixed skill vocabulary
SKILL_VOCAB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data science", "sql", "django", "flask", "nlp",
    "tensorflow", "pytorch", "react", "node", "git", "docker"
]

def score_resume_against_jd(resume_text, jd_text):
    """
    Stable rule-based ATS scoring
    (skill-match only)
    """

    skill_result = compute_skill_match(
        resume_text,
        jd_text,
        SKILL_VOCAB
    )

    ats_score = skill_result["match_percent"]

    return {
        "ats_score": round(ats_score, 2),
        "matched_skills": skill_result["matched_skills"],
        "missing_skills": skill_result["missing_skills"],
        "resume_skills": skill_result["resume_skills"],
        "jd_skills": skill_result["jd_skills"],
        "timestamp": str(datetime.now())
    }
