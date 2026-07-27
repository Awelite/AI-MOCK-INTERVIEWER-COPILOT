
from ats.hybrid_ats import run_hybrid_ats

def run_ats_pipeline(resume_text, jd_text):
    """
    Full ATS pipeline for Interviewer
    """

    ats_out = run_hybrid_ats(resume_text, jd_text)

    score = ats_out["final_ats_score"]

    if score >= 80:
        difficulty = "hard"
    elif score >= 60:
        difficulty = "medium"
    else:
        difficulty = "easy"

    return {
        "ats_score": score,
        "difficulty": difficulty,
        "details": ats_out
    }
