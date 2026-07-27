from statistics import mean


class AnalyticsEngine:

    # ---------------------------------
    # PERFORMANCE ANALYTICS
    # ---------------------------------

    def analyze_candidate_progress(
        self,
        history
    ):

        if len(history) == 0:

            return {
                "error":
                    "No history found"
            }

        scores = []

        for record in history:

            scores.append(
                record[
                    "overall_score"
                ]
            )

        average_score = round(
            mean(scores),
            2
        )

        highest_score = max(scores)

        lowest_score = min(scores)

        latest_score = scores[-1]

        first_score = scores[0]

        # ---------------------------------
        # IMPROVEMENT DETECTION
        # ---------------------------------

        improvement = (
            latest_score - first_score
        )

        if improvement > 10:

            growth = (
                "Strong Improvement"
            )

        elif improvement > 0:

            growth = (
                "Moderate Improvement"
            )

        elif improvement == 0:

            growth = (
                "Stable Performance"
            )

        else:

            growth = (
                "Performance Declined"
            )

        # ---------------------------------
        # CONSISTENCY
        # ---------------------------------

        consistency_gap = (
            highest_score - lowest_score
        )

        if consistency_gap <= 5:

            consistency = (
                "Highly Consistent"
            )

        elif consistency_gap <= 15:

            consistency = (
                "Moderately Consistent"
            )

        else:

            consistency = (
                "Unstable Performance"
            )

        # ---------------------------------
        # RECRUITER INSIGHT
        # ---------------------------------

        if average_score >= 85:

            recruiter_insight = (
                "High-potential candidate"
            )

        elif average_score >= 70:

            recruiter_insight = (
                "Promising candidate"
            )

        else:

            recruiter_insight = (
                "Needs significant improvement"
            )

        # ---------------------------------
        # FINAL ANALYTICS
        # ---------------------------------

        return {

            "average_score":
                average_score,

            "highest_score":
                highest_score,

            "lowest_score":
                lowest_score,

            "latest_score":
                latest_score,

            "growth_trend":
                growth,

            "consistency":
                consistency,

            "recruiter_insight":
                recruiter_insight
        }