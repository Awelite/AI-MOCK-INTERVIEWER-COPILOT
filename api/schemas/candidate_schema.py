from pydantic import BaseModel


class CandidateRequest(BaseModel):

    candidate_id: str

    ats_score: int

    coding_score: int

    semantic_score: int