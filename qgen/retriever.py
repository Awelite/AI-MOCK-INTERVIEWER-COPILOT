import os
import numpy as np
import pandas as pd



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


# ── Lazy-load state ──────────────────────────────────────────────────────────
# Nothing is loaded at import time. First call to _get_retriever_state()
# initialises everything. Keeps startup instant.
# ─────────────────────────────────────────────────────────────────────────────

_embedder   = None
_df_q       = None
_embeddings = None


def _get_retriever_state():
    global _embedder, _df_q, _embeddings
    if _embedder is None:
        print("[qgen] Loading Question Retriever (lazy)...")
        from sentence_transformers import SentenceTransformer
        _embedder   = SentenceTransformer("all-MiniLM-L6-v2")
        _df_q       = pd.read_csv(CSV_PATH)
        _embeddings = np.load(EMBEDDINGS_PATH)
        print("[qgen] Question Retriever loaded.")
    return _embedder, _df_q, _embeddings


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

    embedder, df_q, embeddings = _get_retriever_state()

    query_emb = embedder.encode(
        [query],
        convert_to_numpy=True
    )

    from sklearn.metrics.pairwise import cosine_similarity

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