from coding_round.testcase_loader import (
    TestCaseLoader
)

from coding_round.judge0_client import (
    Judge0Client
)

from coding_round.ai_review import (
    generate_ai_review
)


class CodingEngine:

    def __init__(self):

        self.test_loader = (
            TestCaseLoader()
        )

        self.judge0 = (
            Judge0Client()
        )

    def evaluate_submission(

        self,

        problem,

        code,

        language

    ):

        problem_id = (
            problem["id"]
        )

        test_cases = (

            self.test_loader
            .load_testcases(
                problem_id
            )
        )

        passed = 0

        total = len(
            test_cases
        )

        for test in test_cases:

            result = (

            self.judge0.run_code(

                code,

                language,

                test[
                    "input_data"
                ]
            )
        )

            stdout = result.get("stdout")
            stderr = result.get("stderr")

            if stderr:
                print("\nJUDGE0 ERROR:")
                print(stderr)

            actual_output = stdout.strip() if stdout else ""
            expected_output = test["expected_output"].strip()
            
            act_norm = actual_output.replace(" ", "").replace("\"", "'").lower()
            exp_norm = expected_output.replace(" ", "").replace("\"", "'").lower()

            if act_norm == exp_norm:
                passed += 1

        score = round(

            (passed / total) * 100,

            2
        )

        verdict = (

            "Accepted"

            if passed == total

            else

            "Failed"
        )

        review = (

            generate_ai_review(

                problem[
                    "description"
                ],

                code,

                verdict
            )
        )

        return {

            "score": score,

            "passed": passed,

            "total": total,

            "verdict": verdict,

            "ai_review": review
        }