from module8.orchestrator.transition_manager import (
    TransitionManager
)

manager = (
    TransitionManager()
)

result = (
    manager.decide_transition
            (

                level="WEAK",
                coding_score=30,
                semantic_score=25
            )
)

print("\nTransition Decision:\n")

print(result)