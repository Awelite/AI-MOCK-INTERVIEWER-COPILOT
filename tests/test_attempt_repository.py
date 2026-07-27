from coding_round.attempt_repository import (
    AttemptRepository
)

repo = AttemptRepository()

repo.save_attempt(

    user_id=1,

    problem_id=32,

    language="python",

    code='print("hello")',

    passed_tests=1,

    total_tests=1,

    score=100
)

print(
    "Attempt Saved"
)