class CodingFinalReport:

    def generate(

        self,

        session_scores,

        attempted_problems

    ):

        average_score = round(

            sum(session_scores)
            /
            len(session_scores),

            2

        )

        best_score = max(
            session_scores
        )

        weakest_problem = None

        if session_scores:

            weakest_index = (

                session_scores.index(
                    min(session_scores)
                )
            )

            weakest_problem = (

                attempted_problems[
                    weakest_index
                ]
            )

        return {

            "questions_attempted":

                len(
                    session_scores
                ),

            "average_score":

                average_score,

            "best_score":

                best_score,

            "weakest_problem":

                weakest_problem,

            "recommendation":

                self.generate_recommendation(
                    average_score
                )
        }

    def generate_recommendation(

        self,

        score

    ):

        if score >= 80:

            return (
                "Strong coding skills"
            )

        elif score >= 60:

            return (
                "Average coding skills"
            )

        else:

            return (
                "Needs coding practice"
            )