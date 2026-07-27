from qgen.qgen_engine import (
    QGenEngine
)


ats_result = {

    "missing_skills": [
        "aws"
    ],

    "weak_skills": [
        "system design"
    ],

    "topic":
    "Backend Development",

    "difficulty":
    "medium",

    "resume_summary":
    "Python FastAPI developer",

    "jd_summary":
    "AWS Docker SQL Backend Engineer"
}


engine = QGenEngine()

result = engine.generate_questions(
    ats_result
)

print(
    "\nFINAL RESULT:\n"
)

print(result)