class CodingSessionManager:

    def __init__(

        self,

        total_questions=1

    ):

        self.total_questions = (
            total_questions
        )

        self.current_question = 0

        self.scores = []

    def add_score(

        self,

        score

    ):

        self.scores.append(
            score
        )

        self.current_question += 1

    def is_finished(self):

        return (

            self.current_question
            >=
            self.total_questions

        )

    def final_score(self):

        if not self.scores:

            return 0

        return round(

            sum(self.scores)
            /
            len(self.scores),

            2
        )