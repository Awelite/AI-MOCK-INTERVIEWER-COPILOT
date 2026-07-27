class AssessmentPlanner:

    SKILL_TO_CODING_TOPIC = {

        "sql": "hashing",

        "database": "hashing",

        "mysql": "hashing",

        "postgresql": "hashing",

        "aws": "graphs",

        "cloud": "graphs",

        "docker": "graphs",

        "kubernetes": "graphs",

        "system design": "graphs",

        "backend": "dp",

        "api": "dp",

        "rest": "dp",

        "python": "arrays",

        "java": "arrays",

        "c++": "arrays",

        "dsa": "arrays"
    }

    def recommend_assessment(
        self,
        ats_result,
        job_description=""
    ):

        ats_score = ats_result.get(
            "ats_score",
            50
        )

        details = ats_result.get(
            "details",
            {}
        )

        rule_details = details.get(
            "rule_details",
            {}
        )

        missing_skills = rule_details.get(
            "missing_skills",
            []
        )

        # ------------------
        # Difficulty
        # ------------------

        if ats_score >= 80:

            difficulty = "hard"

        elif ats_score >= 60:

            difficulty = "medium"

        else:

            difficulty = "easy"

        # ------------------
        # Topic Selection
        # ------------------

        topic = "arrays"

        if missing_skills:

            skill = (
                missing_skills[0]
                .lower()
                .strip()
            )

            topic = (
                self.SKILL_TO_CODING_TOPIC
                .get(
                    skill,
                    "arrays"
                )
            )

        else:

            jd_lower = (
                job_description.lower()
                if job_description
                else ""
            )

            if (
                "react" in jd_lower
                or
                "javascript" in jd_lower
            ):

                topic = "arrays"

            elif (
                "sql" in jd_lower
                or
                "database" in jd_lower
            ):

                topic = "hashing"

            elif (
                "aws" in jd_lower
                or
                "cloud" in jd_lower
                or
                "docker" in jd_lower
            ):

                topic = "graphs"

            elif (
                "backend" in jd_lower
                or
                "api" in jd_lower
            ):

                topic = "dp"

        return {

            "topic": topic,

            "difficulty": difficulty,

            "reason":
            f"Based on an ATS score of {ats_score}/100 and missing skills, recommending a {difficulty} problem on {topic}."
        }