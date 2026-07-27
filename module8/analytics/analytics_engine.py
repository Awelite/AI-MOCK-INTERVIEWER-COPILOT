class AnalyticsEngine:

    def generate_report(
        self,
        history
    ):

        scores = []

        for item in history:

            scores.append(
                item["overall_score"]
            )

        average_score = (
            sum(scores) / len(scores)
        )

        highest_score = max(scores)

        lowest_score = min(scores)

        latest_score = scores[-1]

        # PERFORMANCE TREND

        if latest_score > average_score:

            trend = "Improving"

        elif latest_score < average_score:

            trend = "Declining"

        else:

            trend = "Stable Performance"

        # CONSISTENCY

        spread = (
            highest_score - lowest_score
        )

        if spread <= 5:

            consistency = (
                "Highly Consistent"
            )

        elif spread <= 15:

            consistency = (
                "Moderately Consistent"
            )

        else:

            consistency = (
                "Inconsistent"
            )

        # RECRUITER INSIGHT

        if average_score >= 85:

            insight = (
                "Excellent candidate"
            )

        elif average_score >= 70:

            insight = (
                "Promising candidate"
            )

        else:

            insight = (
                "Needs improvement"
            )

        return {

            "average_score":
                round(average_score, 2),

            "highest_score":
                highest_score,

            "lowest_score":
                lowest_score,

            "latest_score":
                latest_score,

            "growth_trend":
                trend,

            "consistency":
                consistency,

            "recruiter_insight":
                insight
        }