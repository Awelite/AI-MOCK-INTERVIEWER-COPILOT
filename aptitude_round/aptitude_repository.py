from coding_round.database import get_db


class AptitudeRepository:

    def save_attempt(

        self,

        candidate_id,

        result

    ):

        conn = get_db()

        cursor = conn.cursor()

        cursor.execute(

            """
            INSERT INTO aptitude_attempts
            (
                candidate_id,
                total_questions,
                correct,
                incorrect,
                accuracy_percent
            )
            VALUES
            (%s,%s,%s,%s,%s)
            """,

            (

                candidate_id,

                result["total_questions"],

                result["correct"],

                result["incorrect"],

                result["accuracy_percent"]

            )
        )

        conn.commit()

        cursor.close()

        conn.close()