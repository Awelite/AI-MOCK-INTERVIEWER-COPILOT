from qgen.retriever import (
    retrieve_questions_for_ats
)

from qgen.prompt_builder import (
    build_llm_prompt
)


fake_ats = {

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
    "Python developer with FastAPI",

    "jd_summary":
    "Backend Engineer AWS Docker SQL"
}

retrieved = retrieve_questions_for_ats(
    fake_ats
)

prompt = build_llm_prompt(
    fake_ats,
    retrieved
)

print(prompt)