from coding_round.database import (
    get_db
)


class ProblemSelector:

    def select_problem(self, topic, difficulty, exclude_ids=None):
        if exclude_ids is None:
            exclude_ids = []
            
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Build exclusion clause
        if exclude_ids:
            format_strings = ','.join(['%s'] * len(exclude_ids))
            exclude_clause = f"AND id NOT IN ({format_strings})"
            params = [topic, difficulty] + exclude_ids
            fallback_params = [topic] + exclude_ids
        else:
            exclude_clause = ""
            params = [topic, difficulty]
            fallback_params = [topic]

        query = f"""
            SELECT *
            FROM coding_problems
            WHERE topic=%s
            AND difficulty=%s
            {exclude_clause}
            ORDER BY RAND()
            LIMIT 1
        """
        cursor.execute(query, tuple(params))
        problem = cursor.fetchone()

        if not problem:
            fallback_query = f"""
                SELECT *
                FROM coding_problems
                WHERE topic=%s
                {exclude_clause}
                ORDER BY RAND()
                LIMIT 1
            """
            cursor.execute(fallback_query, tuple(fallback_params))
            problem = cursor.fetchone()

        cursor.close()

        conn.close()

        return problem