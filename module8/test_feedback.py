from module8.feedback.feedback_engine import (
    FeedbackEngine
)

feedback_engine = FeedbackEngine()

pipeline_result = {

    "overall_score": 83,

    "difficulty": "medium",

    "recommendation":
        "Proceed to Final HR Round"
}

result = feedback_engine.generate_feedback(
    pipeline_result
)

print("\nFEEDBACK REPORT:\n")

print(result)