class TransitionManager:

    def decide_transition(

        self,

        level,
        coding_score,
        semantic_score

    ):

        if (
            level == "EXCELLENT"
            and coding_score >= 85
        ):

            return {

                "action":
                "FAST_TRACK",

                "next_round":
                "ADVANCED_TECHNICAL"
            }

        elif (
            semantic_score < 50
        ):

            return {

                "action":
                "REPEAT",

                "next_round":
                "TECHNICAL"
            }

        elif (
            level == "WEAK"
            and coding_score < 40
        ):

            return {

                "action":
                "TERMINATE",

                "next_round":
                "END"
            }

        else:

            return {

                "action":
                "NORMAL",

                "next_round":
                "HR"
            }