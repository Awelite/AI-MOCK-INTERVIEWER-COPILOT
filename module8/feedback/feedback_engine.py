class FeedbackEngine:

    def generate_feedback(
        self,
        pipeline_result
    ):

        overall_score = pipeline_result[
            "overall_score"
        ]

        recommendation = pipeline_result[
            "recommendation"
        ]

        difficulty = pipeline_result[
            "difficulty"
        ]

        strengths = []
        weaknesses = []

        # -----------------------------
        # STRENGTH ANALYSIS
        # -----------------------------

        if overall_score >= 80:

            strengths.append(
                "Strong technical understanding"
            )

            strengths.append(
                "Good interview readiness"
            )

        if difficulty == "hard":

            strengths.append(
                "Handled difficult questions"
            )

        # -----------------------------
        # WEAKNESS ANALYSIS
        # -----------------------------

        if overall_score < 70:

            weaknesses.append(
                "Needs improvement in technical concepts"
            )

        if difficulty == "easy":

            weaknesses.append(
                "Could not progress to harder rounds"
            )

        # -----------------------------
        # COMMUNICATION ANALYSIS
        # -----------------------------

        if overall_score >= 75:

            communication = (
                "Communication confidence appears good"
            )

        else:

            communication = (
                "Communication confidence needs improvement"
            )

        # -----------------------------
        # HIRING CONFIDENCE
        # -----------------------------

        hiring_confidence = (
            f"{overall_score}%"
        )

        # -----------------------------
        # FINAL FEEDBACK OBJECT
        # -----------------------------

        return {

            "overall_score": overall_score,

            "strengths": strengths,

            "weaknesses": weaknesses,

            "communication_analysis":
                communication,

            "difficulty_level":
                difficulty,

            "recommendation":
                recommendation,

            "hiring_confidence":
                hiring_confidence
        }