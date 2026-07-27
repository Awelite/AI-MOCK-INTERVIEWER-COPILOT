class AptitudeReportGenerator:

    def generate(

        self,

        aptitude_result

    ):

        accuracy = (

            aptitude_result[
                "accuracy_percent"
            ]
        )

        if accuracy >= 80:

            recommendation = (

                "Strong Analytical Skills"
            )

        elif accuracy >= 60:

            recommendation = (

                "Average Aptitude Performance"
            )

        else:

            recommendation = (

                "Needs Aptitude Practice"
            )

        return {

            "questions_attempted":

            aptitude_result[
                "total_questions"
            ],

            "correct":

            aptitude_result[
                "correct"
            ],

            "incorrect":

            aptitude_result[
                "incorrect"
            ],

            "accuracy":

            accuracy,

            "recommendation":

            recommendation
        }