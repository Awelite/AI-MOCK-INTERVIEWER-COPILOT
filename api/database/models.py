from sqlalchemy import Column

from sqlalchemy import Integer

from sqlalchemy import String

from api.database.db import Base


class CandidateResult(Base):

    __tablename__ = "candidate_results"


    id = Column(

        Integer,

        primary_key=True,

        index=True
    )

    candidate_id = Column(
        String
    )

    overall_score = Column(
        Integer
    )

    verdict = Column(
        String
    )