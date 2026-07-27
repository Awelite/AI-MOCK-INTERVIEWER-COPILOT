from module8.schemas.interview_schema import (
    CandidateInterview,
    ATSData,
    CodingData,
    TechnicalAnswer,
    HRAnswer
)

from module8.orchestrator.master_pipeline import (
    MasterPipeline
)

candidate = CandidateInterview(

    candidate_id="CAND_001",

    ats=ATSData(
        extracted_skills=[
            "Python",
            "SQL",
            "FastAPI"
        ],
        ats_score=82
    ),

    coding=CodingData(
        passed=8,
        total=10,
        time_taken=100,
        errors=1
    ),

    technical=[

        TechnicalAnswer(
            question="What is normalization?",
            expected_answer=
            "Removes redundancy",

            user_answer=
            "Normalization reduces duplicate data"
        )
    ],

    hr=[

        HRAnswer(
            question=
            "Tell me about yourself",

            user_answer=
            "I am a backend engineer"
        )
    ]
)

pipeline = MasterPipeline()

result = (
    pipeline.run_pipeline(
        candidate
    )
)

print("\nFINAL RESULT:\n")

print(result)