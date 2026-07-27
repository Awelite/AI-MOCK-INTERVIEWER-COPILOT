from fastapi import APIRouter

router = APIRouter()


@router.get("/executive-summary")

def executive_summary():

    return {

        "summary":

        """
Candidate demonstrates strong backend
fundamentals with moderate communication
skills.

Recommended for junior backend
engineering roles after additional
DSA preparation.
        """
    }