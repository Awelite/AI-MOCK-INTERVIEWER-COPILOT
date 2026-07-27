from qgen.retriever import (
    retrieve_questions_for_ats
)


fake_ats = {

    "missing_skills": [

        "aws",

        "cloud security"
    ],

    "weak_skills": [

        "system design"
    ],

    "topic":

    "Backend Development",

    "difficulty":

    "medium"
}


result = retrieve_questions_for_ats(
    fake_ats
)


print(
    "\nTOP RETRIEVED QUESTIONS:\n"
)

print(

    result[
        [
            "skill",
            "question_text_clean",
            "similarity"
        ]
    ].head(15)
)