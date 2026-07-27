from coding_round.database import (
    get_db
)


class TestCaseLoader:

    def load_testcases(
        self,
        problem_id
    ):

        conn = get_db()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                input_data,
                expected_output,
                is_hidden
            FROM test_cases
            WHERE problem_id=%s
            """,
            (problem_id,)
        )

        rows = cursor.fetchall()

        cursor.close()

        conn.close()

        return rows