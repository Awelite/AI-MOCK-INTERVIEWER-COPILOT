from fastapi import APIRouter

from fastapi import Depends

from sqlalchemy.orm import Session

from api.database.db import (
    get_db
)

from api.database.models import (
    CandidateResult
)

router = APIRouter()


# GET ALL CANDIDATES

@router.get("/candidates")

def get_candidates(

    db: Session = Depends(get_db)
):

    candidates = db.query(
        CandidateResult
    ).all()


    results = []


    for candidate in candidates:

        results.append({

            "id": candidate.id,

            "candidate_id":

            candidate.candidate_id,

            "overall_score":

            candidate.overall_score,

            "verdict":

            candidate.verdict
        })


    return results


# GET SINGLE CANDIDATE

@router.get("/candidate/{candidate_id}")

def get_candidate(

    candidate_id: str,

    db: Session = Depends(get_db)
):

    candidate = db.query(
        CandidateResult
    ).filter(

        CandidateResult.candidate_id
        == candidate_id

    ).first()


    if not candidate:

        return {

            "message":

            "Candidate not found"
        }


    return {

        "id": candidate.id,

        "candidate_id":

        candidate.candidate_id,

        "overall_score":

        candidate.overall_score,

        "verdict":

        candidate.verdict
    }