from ats.score import score_resume_against_jd
from ats.ml_based_ats import run_ml_based_ats


def run_hybrid_ats(resume_text, jd_text):
    """
    Hybrid ATS = 30% Rule-based + 70% ML-based
    """

    # Rule-based ATS
    rule_out = score_resume_against_jd(resume_text, jd_text)
    rule_score = rule_out["ats_score"]  # 0-100

    # ML-based ATS
    ml_out = run_ml_based_ats(resume_text, jd_text)
    ml_score = ml_out["ml_score"]       # 0-100

    # Hybrid merge
    final_score = round(
        0.3 * rule_score + 0.7 * ml_score,
        2
    )

    return {
        "final_ats_score": final_score,
        "rule_score": rule_score,
        "ml_score": ml_score,
        "rule_details": rule_out,
        "ml_details": ml_out
    }
