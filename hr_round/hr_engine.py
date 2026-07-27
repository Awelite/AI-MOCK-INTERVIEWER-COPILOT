import random

from hr_round.hr_questions import (
    HR_QUESTIONS
)

from hr_round.hr_scorer import (
    evaluate_answer
)

from hr_round.hr_dataset import (
    HR_DATASET
)


class HREngine:

    # --------------------------------------------------
    # get_questions(count)
    # Returns a list of `count` randomly selected HR
    # questions WITHOUT evaluating anything.
    # Called by GET /hr/questions/{session_id}
    # --------------------------------------------------

    def get_questions(
        self,
        count: int = 3
    ) -> list:

        count = min(count, len(HR_QUESTIONS))

        return random.sample(
            HR_QUESTIONS,
            count
        )

    # --------------------------------------------------
    # evaluate_answers(questions, answers)
    # Evaluates a parallel list of (question, answer)
    # pairs and returns structured result dicts.
    # Called by POST /hr/submit
    # --------------------------------------------------

    def evaluate_answers(
        self,
        questions: list,
        answers: list
    ) -> list:

        results = []

        for question, answer in zip(
            questions,
            answers
        ):

            ideal_answer = (
                HR_DATASET.get(
                    question,
                    ""
                )
            )

            evaluation = (
                evaluate_answer(
                    answer,
                    ideal_answer
                )
            )

            results.append({
                "question": question,
                "answer": answer,
                "evaluation": evaluation
            })

        return results

    # --------------------------------------------------
    # conduct_round(answers)
    # Legacy method — preserved for backward compat.
    # Selects questions internally and evaluates at once.
    # --------------------------------------------------

    def conduct_round(
        self,
        answers
    ):

        results = []

        selected_questions = (

            random.sample(

                HR_QUESTIONS,

                len(answers)

            )
        )

        for question, answer in zip(

            selected_questions,

            answers

        ):

            ideal_answer = (

                HR_DATASET.get(

                    question,

                    ""

                )
            )

            evaluation = (

                evaluate_answer(

                    answer,

                    ideal_answer

                )
            )

            results.append({

                "question": question,

                "answer": answer,

                "evaluation": evaluation

            })

        return results