from coding_round.problem_selector import (
    ProblemSelector
)

selector = ProblemSelector()

problem = selector.select_problem(

    topic="arrays",

    difficulty="easy"
)

print(problem)