import os
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer


BASE_DIR = os.path.dirname(__file__)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "sbert_lgbm"
)


SBERT_PATH = os.path.join(
    MODEL_DIR,
    "sbert_encoder"
)

LGBM_PATH = os.path.join(
    MODEL_DIR,
    "lgbm_model.pkl"
)


print("Loading ATS ML models...")

sbert = SentenceTransformer(
    SBERT_PATH
)

lgbm_model = joblib.load(
    LGBM_PATH
)


def run_ml_based_ats(
    resume_text,
    jd_text
):

    emb_resume = sbert.encode(
        resume_text
    )

    emb_jd = sbert.encode(
        jd_text
    )

    features = np.abs(
        emb_resume - emb_jd
    ).reshape(1, -1)

    prob = float(
        lgbm_model.predict(features)[0]
    )

    ml_score = round(
        prob * 100,
        2
    )

    return {
        "ml_score": ml_score
    }