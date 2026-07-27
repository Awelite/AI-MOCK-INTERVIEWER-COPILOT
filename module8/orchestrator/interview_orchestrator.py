from enum import Enum


class InterviewState(Enum):

    ATS = "ATS"

    CODING = "CODING"

    TECHNICAL = "TECHNICAL"

    ADVANCED_TECHNICAL = (
        "ADVANCED_TECHNICAL"
    )

    HR = "HR"

    FINAL = "FINAL"

    END = "END"


class InterviewOrchestrator:

    def __init__(self):

        self.current_state = (
            InterviewState.ATS
        )

    def evaluate_candidate_level(

        self,

        ats_score,

        coding_score,

        aptitude_score,

        semantic_score=75,

        hr_score=75

    ):

        total = (

            ats_score * 0.20 +

            coding_score * 0.40 +

            aptitude_score * 0.20 +

            semantic_score * 0.10 +

            hr_score * 0.10

        )

        if total >= 85:

            return "EXCELLENT"

        elif total >= 70:

            return "GOOD"

        elif total >= 50:

            return "AVERAGE"

        else:

            return "WEAK"

    def next_round(

        self,
        level=None

    ):

        if self.current_state == (
            InterviewState.ATS
        ):

            self.current_state = (
                InterviewState.CODING
            )

        elif self.current_state == (
            InterviewState.CODING
        ):

            if level == "EXCELLENT":

                self.current_state = (
                    InterviewState
                    .ADVANCED_TECHNICAL
                )

            else:

                self.current_state = (
                    InterviewState
                    .TECHNICAL
                )

        elif self.current_state in [

            InterviewState.TECHNICAL,

            InterviewState
            .ADVANCED_TECHNICAL

        ]:

            self.current_state = (
                InterviewState.HR
            )

        elif self.current_state == (
            InterviewState.HR
        ):

            self.current_state = (
                InterviewState.FINAL
            )

        elif self.current_state == (
            InterviewState.FINAL
        ):

            self.current_state = (
                InterviewState.END
            )

        return self.current_state

    def get_current_round(self):

        return (
            self.current_state.value
        )