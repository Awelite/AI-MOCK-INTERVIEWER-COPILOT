from module8.schemas.interview_schema import (
    ATSData,
    CodingData,
    TechnicalAnswer,
    HRAnswer,
    CandidateInterview
)

from module8.core.intelligence_engine import (
    IntelligenceEngine
)


candidate = CandidateInterview(

    candidate_id="123",

    ats=ATSData(
        extracted_skills=[
            "Python",
            "SQL"
        ],
        ats_score=82
    ),

    coding=CodingData(
        passed=8,
        total=10,
        time_taken=120,
        errors=1
    ),

    technical=[

        TechnicalAnswer(

            question="What is normalization?",

            expected_answer=(
                "Normalization removes redundancy"
            ),

            user_answer=(
                "Normalization reduces duplicate data"
            )
        ),

        TechnicalAnswer(

            question="What is indexing?",

            expected_answer=(
                "Indexing improves database search performance"
            ),

            user_answer=(
                "Indexes make queries faster"
            )
        )
    ],

    hr=[

        HRAnswer(

            question="Tell me about yourself",

            user_answer=(
                "I am a backend developer"
            )
        )
    ]
)


engine = IntelligenceEngine()

result = engine.evaluate_candidate(
    candidate
)

print("\nAI Evaluation Result:\n")

print(result)