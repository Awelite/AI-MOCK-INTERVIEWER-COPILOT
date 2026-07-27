class RecruiterDecisionEngine:

    def generate_decision(
        self,
        analytics,
        trends,
        latest_result
    ):

        overall_score = latest_result[
            "overall_score"
        ]

        recommendation = latest_result[
            "recommendation"
        ]

        performance = trends[
            "performance_trend"
        ]

        weaknesses = trends[
            "detected_weaknesses"
        ]

        risk_flags = trends[
            "risk_flags"
        ]

        # ---------------------------------
        # HIRING CONFIDENCE
        # ---------------------------------

        if overall_score >= 85:

            confidence = "High"

        elif overall_score >= 70:

            confidence = "Medium"

        else:

            confidence = "Low"

        # ---------------------------------
        # ROLE FIT
        # ---------------------------------

        if overall_score >= 85:

            role_fit = (
                "Strong Mid-Level Engineer"
            )

        elif overall_score >= 70:

            role_fit = (
                "Junior Developer"
            )

        else:

            role_fit = (
                "Needs More Preparation"
            )

        # ---------------------------------
        # SALARY BAND
        # ---------------------------------

        if overall_score >= 85:

            salary_band = "8-15 LPA"

        elif overall_score >= 70:

            salary_band = "4-8 LPA"

        else:

            salary_band = "Below 4 LPA"

        # ---------------------------------
        # FAST TRACK DETECTION
        # ---------------------------------

        if (
            confidence == "High"
            and len(risk_flags) == 0
        ):

            fast_track = True

        else:

            fast_track = False

        # ---------------------------------
        # RECRUITER NOTES
        # ---------------------------------

        notes = []

        if (
            "Coding Skills"
            in weaknesses
        ):

            notes.append(
                "Needs stronger DSA practice"
            )

        if (
            "Technical Concepts"
            in weaknesses
        ):

            notes.append(
                "Core CS concepts need improvement"
            )

        if len(notes) == 0:

            notes.append(
                "Candidate demonstrates balanced skills"
            )

        # ---------------------------------
        # FINAL VERDICT
        # ---------------------------------

        if (
            confidence == "High"
            and recommendation == "Proceed to Final HR Round"
        ):

            verdict = "Highly Recommended"

        elif confidence == "Medium":

            verdict = "Recommended with Improvements"

        else:

            verdict = "Not Recommended"

        # ---------------------------------
        # FINAL OUTPUT
        # ---------------------------------

        return {

            "hiring_confidence":
                confidence,

            "role_fit":
                role_fit,

            "salary_band":
                salary_band,

            "fast_track":
                fast_track,

            "recruiter_notes":
                notes,

            "final_verdict":
                verdict,

            "performance_trend":
                performance
        }