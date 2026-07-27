from module8.orchestrator.interview_orchestrator import (
    InterviewOrchestrator
)

orchestrator = (
    InterviewOrchestrator()
)

ats_score = 40
coding_score = 45
semantic_score = 50

candidate_level = (
    orchestrator
    .evaluate_candidate_level(

        ats_score,
        coding_score,
        semantic_score
    )
)

print("\nCandidate Level:")
print(candidate_level)

print("\nInterview Flow:\n")

while True:

    current = (
        orchestrator
        .get_current_round()
    )

    print(
        f"Current Round: {current}"
    )

    if current == "END":

        break

    orchestrator.next_round(
        candidate_level
    )