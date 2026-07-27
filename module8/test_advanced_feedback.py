from module8.feedback.advanced_feedback import (
    AdvancedFeedbackEngine
)

engine = AdvancedFeedbackEngine()

pipeline_result = {

    "overall_score": 83,

    "difficulty": "medium",

    "recommendation":
        "Proceed to Final HR Round"
}

result = engine.generate_advanced_feedback(
    pipeline_result
)

print("\nADVANCED FEEDBACK:\n")

print(result)