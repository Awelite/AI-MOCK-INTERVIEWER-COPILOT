import re


def extract_skills(
    text,
    skill_vocab
):

    text = text.lower()

    found = set()

    for skill in skill_vocab:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(
            pattern,
            text
        ):

            found.add(skill)

    return found


def compute_skill_match(

    resume_text,
    jd_text,
    skill_vocab
):

    resume_skills = extract_skills(
        resume_text,
        skill_vocab
    )

    jd_skills = extract_skills(
        jd_text,
        skill_vocab
    )

    matched = resume_skills.intersection(
        jd_skills
    )

    missing = jd_skills - resume_skills

    if len(jd_skills) == 0:

        match_percent = 0

    else:

        match_percent = (

            len(matched)
            /
            len(jd_skills)
        ) * 100

    return {

        "match_percent":

        round(match_percent, 2),

        "matched_skills":

        list(matched),

        "missing_skills":

        list(missing),

        "resume_skills":

        list(resume_skills),

        "jd_skills":

        list(jd_skills)
    }