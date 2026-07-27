import os
import numpy as np
import pandas as pd

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


BASE_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

CSV_PATH = os.path.join(
    DATA_DIR,
    "clean_questions_for_qgen_v2.csv"
)

EMBEDDINGS_PATH = os.path.join(
    DATA_DIR,
    "question_embeddings.npy"
)


print(
    "Loading Question Retriever..."
)

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

df_q = pd.read_csv(
    CSV_PATH
)

embeddings = np.load(
    EMBEDDINGS_PATH
)


def get_skill_query(
    skill,
    topic=None,
    difficulty=None
):

    parts = [skill]

    if topic:
        parts.append(topic)

    if difficulty:
        parts.append(difficulty)

    return " ".join(parts)


def get_top_questions_for_skill(
    skill,
    topic=None,
    difficulty=None,
    top_k=10
):

    query = get_skill_query(
        skill,
        topic,
        difficulty
    )

    query_emb = embedder.encode(
        [query],
        convert_to_numpy=True
    )

    sims = cosine_similarity(
        query_emb,
        embeddings
    )[0]

    top_idx = sims.argsort()[::-1][:top_k]

    results = df_q.iloc[
        top_idx
    ].copy()

    results["similarity"] = (
        sims[top_idx]
    )

    return results.reset_index(
        drop=True
    )


def retrieve_questions_for_ats(
    ats_result,
    per_skill=5
):

    missing = (
    ats_result
    .get("details", {})
    .get("rule_details", {})
    .get("missing_skills", [])
)


    weak = ats_result.get(
        "weak_skills",
        []
    ) or []

    topic = ats_result.get(
        "topic"
    )

    difficulty = ats_result.get(
        "difficulty"
    )

    all_rows = []

    for skill in missing:

        rows = get_top_questions_for_skill(
            skill,
            topic,
            difficulty,
            top_k=per_skill
        )

        rows["source_type"] = (
            "missing_skill"
        )

        rows["skill"] = skill

        all_rows.append(rows)

    for skill in weak:

        rows = get_top_questions_for_skill(
            skill,
            topic,
            difficulty,
            top_k=per_skill
        )

        rows["source_type"] = (
            "weak_skill"
        )

        rows["skill"] = skill

        all_rows.append(rows)

    if not all_rows:

        return pd.DataFrame()

    merged = pd.concat(
        all_rows,
        ignore_index=True
    )

    merged = merged.drop_duplicates(
        subset=[
            "question_text_clean"
        ]
    )

    merged = merged.sort_values(
        by="similarity",
        ascending=False
    )

    return merged.reset_index(
        drop=True
    )