from coding_round.database import (
    get_db
)


class AttemptRepository:

    def save_attempt(

        self,

        user_id,

        problem_id,

        language,

        code,

        passed_tests,

        total_tests,

        score
    ):

        conn = get_db()

        cursor = conn.cursor()

        query = """
        INSERT INTO coding_attempts
        (
            user_id,
            problem_id,
            language,
            code,
            passed_tests,
            total_tests,
            score
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (

            user_id,

            problem_id,

            language,

            code,

            passed_tests,

            total_tests,

            score
        )

        cursor.execute(
            query,
            values
        )

        conn.commit()

        cursor.close()

        conn.close()