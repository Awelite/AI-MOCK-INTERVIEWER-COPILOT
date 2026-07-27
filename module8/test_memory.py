from module8.memory.memory_engine import (
    MemoryEngine
)

memory = MemoryEngine()

pipeline_result = {

    "overall_score": 83,

    "difficulty": "medium",

    "recommendation":
        "Proceed to Final HR Round"
}

advanced_feedback = {

    "technical_depth":
        "Moderate technical understanding",

    "hiring_risk":
        "Medium"
}

# ---------------------------------
# SAVE
# ---------------------------------

result = memory.save_interview(

    candidate_id="CAND_001",

    pipeline_result=pipeline_result,

    advanced_feedback=advanced_feedback
)

print(result)

# ---------------------------------
# FETCH HISTORY
# ---------------------------------

history = memory.get_candidate_history(
    "CAND_001"
)

print("\nCANDIDATE HISTORY:\n")

print(history)