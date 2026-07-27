from fastapi import APIRouter

from fastapi import Depends

from sqlalchemy.orm import Session

from api.schemas.candidate_schema import (
    CandidateRequest
)

from api.services.ai_service import (
    generate_ai_evaluation
)

from api.database.db import (
    get_db
)

router = APIRouter()


@router.post("/evaluate")

def evaluate_candidate(

    request: CandidateRequest,

    db: Session = Depends(get_db)
):

    result = generate_ai_evaluation(

        request,

        db
    )

    return result