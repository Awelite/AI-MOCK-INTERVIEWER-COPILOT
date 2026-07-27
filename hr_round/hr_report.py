class HRReport:

    def generate(

        self,

        hr_results

    ):

        scores = [

            item["evaluation"][
                "hr_score"
            ]

            for item in hr_results
        ]

        avg_score = (

            sum(scores)

            /

            len(scores)

        )

        return {

            "questions": len(scores),

            "average_hr_score":

                round(
                    avg_score,
                    2
                ),

            "recommendation":

                "Strong HR Communication"

                if avg_score >= 70

                else

                "Needs HR Practice"

        }