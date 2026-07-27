class DifficultyController:

    def __init__(self):

        self.levels = {

            "easy": 1,

            "medium": 2,

            "hard": 3
        }

    def adjust_difficulty(

        self,

        coding_score

    ):

        if coding_score >= 80:

            return "hard"

        elif coding_score >= 50:

            return "medium"

        else:

            return "easy"

    def get_next_difficulty(

        self,

        current_difficulty,

        coding_score

    ):

        new_difficulty = (
            self.adjust_difficulty(
                coding_score
            )
        )

        return new_difficulty