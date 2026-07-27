from schemas.interview_schema import *

sample = InterviewInput(
    candidate_id="123",

    ats={
        "extracted_skills": ["Python", "SQL"],
        "ats_score": 78
    },

    coding={
        "passed": 7,
        "total": 10,
        "time_taken": 120,
        "errors": 2
    },

    technical=[
        {
            "question": "What is normalization?",
            "expected_answer": "Removes redundancy",
            "user_answer": "It reduces duplicate data"
        }
    ],

    hr=[
        {
            "question": "Tell me about yourself",
            "user_answer": "I am a backend developer"
        }
    ]
)

print(sample)