class ExecutiveSummaryGenerator:

    def generate_summary(
        self,
        recruiter_report,
        analytics_report,
        feedback_report
    ):

        confidence = recruiter_report[
            "hiring_confidence"
        ]

        role_fit = recruiter_report[
            "role_fit"
        ]

        trend = recruiter_report[
            "performance_trend"
        ]

        strengths = feedback_report[
            "strengths"
        ]

        weaknesses = feedback_report[
            "weaknesses"
        ]

        average_score = analytics_report[
            "average_score"
        ]

        summary = f"""

Candidate Evaluation Summary
----------------------------

Overall Performance Score:
{average_score}

Hiring Confidence:
{confidence}

Recommended Role:
{role_fit}

Performance Trend:
{trend}

Key Strengths:
- {strengths[0]}
- {strengths[1]}

Areas for Improvement:
- {weaknesses[0]}
- {weaknesses[1]}

Final Recruiter Insight:
Candidate demonstrates good technical capability
with promising interview potential.

Recommended for further consideration.

"""

        return summary