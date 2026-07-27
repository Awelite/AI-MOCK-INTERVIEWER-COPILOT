from module8.core.assessment_planner import (
    AssessmentPlanner
)

planner = AssessmentPlanner()

ats_result = {

    "ats_score": 72,

    "details": {

        "rule_details": {

            "missing_skills": [
                "sql"
            ]
        }
    }
}

result = planner.recommend_assessment(

    ats_result,

    "Backend Engineer with SQL and Docker"
)

print(result)