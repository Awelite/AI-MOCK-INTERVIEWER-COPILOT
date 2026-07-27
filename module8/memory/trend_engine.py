class TrendEngine:

    def detect_trends(
        self,
        history
    ):

        if len(history) == 0:

            return {
                "error":
                    "No candidate history found"
            }

        weaknesses = []

        risk_flags = []

        scores = []

        # ---------------------------------
        # ANALYZE HISTORY
        # ---------------------------------

        for record in history:

            score = record[
                "overall_score"
            ]

            scores.append(score)

            feedback = record[
                "advanced_feedback"
            ]

            # -----------------------------
            # CODING READINESS
            # -----------------------------

            coding = feedback.get(
                "coding_readiness",
                ""
            )

            if (
                "practice"
                in coding.lower()
            ):

                weaknesses.append(
                    "Coding Skills"
                )

            # -----------------------------
            # TECHNICAL DEPTH
            # -----------------------------

            technical = feedback.get(
                "technical_depth",
                ""
            )

            if (
                "weak"
                in technical.lower()
            ):

                weaknesses.append(
                    "Technical Concepts"
                )

            # -----------------------------
            # HIRING RISK
            # -----------------------------

            risk = feedback.get(
                "hiring_risk",
                ""
            )

            if risk == "High":

                risk_flags.append(
                    "High Hiring Risk"
                )

        # ---------------------------------
        # SCORE TREND
        # ---------------------------------

        latest_score = scores[-1]

        average_score = (
            sum(scores) / len(scores)
        )

        if latest_score > average_score:

            performance_trend = (
                "Improving Candidate"
            )

        elif latest_score < average_score:

            performance_trend = (
                "Declining Candidate"
            )

        else:

            performance_trend = (
                "Stable Candidate"
            )

        # ---------------------------------
        # UNIQUE ISSUES
        # ---------------------------------

        weaknesses = list(
            set(weaknesses)
        )

        risk_flags = list(
            set(risk_flags)
        )

        # ---------------------------------
        # IMPROVEMENT PRIORITY
        # ---------------------------------

        if (
            "Coding Skills"
            in weaknesses
        ):

            priority = (
                "Improve coding problem-solving"
            )

        elif (
            "Technical Concepts"
            in weaknesses
        ):

            priority = (
                "Strengthen core CS fundamentals"
            )

        else:

            priority = (
                "Continue advanced preparation"
            )

        # ---------------------------------
        # FINAL REPORT
        # ---------------------------------

        return {

            "performance_trend":
                performance_trend,

            "detected_weaknesses":
                weaknesses,

            "risk_flags":
                risk_flags,

            "priority_action":
                priority
        }