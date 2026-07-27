from module8.schemas.interview_schema import (
    CandidateInterview,
    ATSData,
    CodingData,
    TechnicalAnswer,
    HRAnswer
)

from module8.core.intelligence_engine import (
    IntelligenceEngine
)

candidate = CandidateInterview(

    candidate_id="C101",

    ats=ATSData(
        extracted_skills=["Python"],
        ats_score=80
    ),

    coding=CodingData(
        passed=8,
        total=10,
        time_taken=100,
        errors=1
    ),

    technical=[

        TechnicalAnswer(

            question=
            "What is normalization?",

            expected_answer=
            "Normalization removes redundancy in databases",

            user_answer=
            "Normalization improves consistency and reduces duplicate data"
        )
    ],

    hr=[

        HRAnswer(
            question="Tell me about yourself",
            user_answer="I am a backend developer"
        )
    ]
)

engine = IntelligenceEngine()

result = engine.evaluate_candidate(
    candidate
)

print("\nAI Evaluation Result:\n")

print(result)