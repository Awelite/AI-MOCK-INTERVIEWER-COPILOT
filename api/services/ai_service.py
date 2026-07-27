from api.database.models import (
    CandidateResult
)


def generate_ai_evaluation(

    data,

    db
):

    overall_score = (

        data.ats_score +

        data.coding_score +

        data.semantic_score

    ) / 3


    if overall_score >= 85:

        verdict = "Strong Hire"

    elif overall_score >= 70:

        verdict = "Recommended"

    else:

        verdict = "Needs Improvement"


    # DATABASE SAVE

    candidate = CandidateResult(

        candidate_id=data.candidate_id,

        overall_score=round(
            overall_score
        ),

        verdict=verdict
    )


    db.add(candidate)

    db.commit()

    db.refresh(candidate)


    return {

        "candidate_id":

        data.candidate_id,

        "overall_score":

        round(overall_score, 2),

        "verdict":

        verdict
    }