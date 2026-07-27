from module8.orchestrator.difficulty_controller import (
    DifficultyController
)

controller = DifficultyController()

print(
    controller.adjust_difficulty(90)
)

print(
    controller.adjust_difficulty(65)
)

print(
    controller.adjust_difficulty(30)
)