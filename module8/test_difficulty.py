from module8.orchestrator.difficulty_controller import (
    DifficultyController
)

controller = (
    DifficultyController()
)

ats_score = 40
coding_score = 45
semantic_score = 50

difficulty = (
    controller.determine_difficulty(

        ats_score,
        coding_score,
        semantic_score
    )
)

strategy = (
    controller.generate_followup_strategy(

        difficulty,
        weak_topic="Recursion"
    )
)

print("\nDifficulty Level:")
print(difficulty)

print("\nAdaptive Strategy:")
print(strategy)