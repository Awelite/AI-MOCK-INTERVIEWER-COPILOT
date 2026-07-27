class AdvancedFeedbackEngine:

    def generate_advanced_feedback(
        self,
        pipeline_result
    ):

        overall_score = pipeline_result[
            "overall_score"
        ]

        difficulty = pipeline_result[
            "difficulty"
        ]

        recommendation = pipeline_result[
            "recommendation"
        ]

        # ---------------------------------
        # TECHNICAL DEPTH
        # ---------------------------------

        if overall_score >= 85:

            technical_depth = (
                "Excellent understanding of technical concepts"
            )

        elif overall_score >= 70:

            technical_depth = (
                "Moderate technical understanding"
            )

        else:

            technical_depth = (
                "Weak technical understanding"
            )

        # ---------------------------------
        # CODING READINESS
        # ---------------------------------

        if difficulty == "hard":

            coding_readiness = (
                "Ready for advanced coding interviews"
            )

        elif difficulty == "medium":

            coding_readiness = (
                "Ready for intermediate coding rounds"
            )

        else:

            coding_readiness = (
                "Needs more coding practice"
            )

        # ---------------------------------
        # CONFIDENCE ESTIMATION
        # ---------------------------------

        confidence_score = round(
            overall_score * 0.95,
            2
        )

        # ---------------------------------
        # INTERVIEW READINESS
        # ---------------------------------

        if overall_score >= 80:

            readiness = (
                "Industry interview ready"
            )

        else:

            readiness = (
                "Requires additional preparation"
            )

        # ---------------------------------
        # IMPROVEMENT ROADMAP
        # ---------------------------------

        roadmap = []

        if overall_score < 80:

            roadmap.append(
                "Practice more coding problems"
            )

            roadmap.append(
                "Improve communication clarity"
            )

        else:

            roadmap.append(
                "Focus on advanced system design"
            )

            roadmap.append(
                "Prepare for leadership discussions"
            )

        # ---------------------------------
        # HIRING RISK
        # ---------------------------------

        if overall_score >= 85:

            hiring_risk = "Low"

        elif overall_score >= 70:

            hiring_risk = "Medium"

        else:

            hiring_risk = "High"

        # ---------------------------------
        # FINAL REPORT
        # ---------------------------------

        return {

            "technical_depth":
                technical_depth,

            "coding_readiness":
                coding_readiness,

            "confidence_score":
                confidence_score,

            "interview_readiness":
                readiness,

            "improvement_roadmap":
                roadmap,

            "hiring_risk":
                hiring_risk,

            "final_recommendation":
                recommendation
        }