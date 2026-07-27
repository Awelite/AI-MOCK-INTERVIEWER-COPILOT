def build_llm_prompt(
    ats_result,
    retrieved_questions,
    num_final=5
):

    resume_summary = ats_result.get(
        "resume_summary",
        ""
    )

    jd_summary = ats_result.get(
        "jd_summary",
        ""
    )

    missing = ats_result.get(
        "missing_skills",
        []
    )

    weak = ats_result.get(
        "weak_skills",
        []
    )

    topic = ats_result.get(
        "topic",
        ""
    )

    difficulty = ats_result.get(
        "difficulty",
        ""
    )

    prompt = f"""
You are an expert technical interviewer.

Generate {num_final} highly relevant interview questions.

Candidate Summary:
{resume_summary}

Job Summary:
{jd_summary}

Missing Skills:
{', '.join(missing)}

Weak Skills:
{', '.join(weak)}

Topic:
{topic}

Difficulty:
{difficulty}

Reference Questions:
"""

    for q in retrieved_questions[
        "question_text_clean"
    ].head(5):

        prompt += f"\n- {q}"

    prompt += """

Generate NEW questions.

Do NOT copy.

Focus mainly on:
1. Missing skills
2. Weak skills
3. Required job skills

Return:

1.
2.
3.
4.
5.
"""

    return prompt