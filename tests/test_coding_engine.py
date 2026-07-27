from coding_round.coding_engine import (
    CodingEngine
)

from coding_round.problem_selector import (
    ProblemSelector
)

problem = (

    ProblemSelector()
    .select_problem(

        topic="hashing",

        difficulty="medium"
    )
)

engine = CodingEngine()

result = (

    engine.evaluate_submission(

        problem,

        """
print("grouped")
""",

        "python"
    )
)

print(result)