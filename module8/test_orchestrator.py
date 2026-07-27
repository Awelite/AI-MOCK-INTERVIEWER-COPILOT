from module8.orchestrator.interview_orchestrator import (
    InterviewOrchestrator
)

orchestrator = (
    InterviewOrchestrator()
)

print("\nStarting Interview\n")

while True:

    current = (
        orchestrator.get_current_round()
    )

    print(
        f"Current Round: {current}"
    )

    if current == "END":

        break

    orchestrator.next_round()