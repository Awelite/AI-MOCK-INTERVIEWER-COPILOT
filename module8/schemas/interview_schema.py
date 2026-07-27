from pydantic import BaseModel
from typing import List


class ATSData(BaseModel):
    extracted_skills: List[str]
    ats_score: float


class CodingData(BaseModel):
    passed: int
    total: int
    time_taken: float
    errors: int


class TechnicalAnswer(BaseModel):
    question: str
    expected_answer: str
    user_answer: str


class HRAnswer(BaseModel):
    question: str
    user_answer: str


class CandidateInterview(BaseModel):

    candidate_id: str

    ats: ATSData

    coding: CodingData

    technical: List[TechnicalAnswer]

    hr: List[HRAnswer]