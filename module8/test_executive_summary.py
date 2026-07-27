from module8.executive.executive_summary import (
    ExecutiveSummaryGenerator
)

generator = ExecutiveSummaryGenerator()

recruiter_report = {

    "hiring_confidence": "Medium",

    "role_fit": "Junior Backend Developer",

    "performance_trend": "Stable Candidate"
}

analytics_report = {

    "average_score": 83
}

feedback_report = {

    "strengths": [

        "Good backend fundamentals",

        "Strong SQL understanding"
    ],

    "weaknesses": [

        "Needs DSA improvement",

        "Communication can improve"
    ]
}

summary = generator.generate_summary(

    recruiter_report,
    analytics_report,
    feedback_report
)

print(summary)