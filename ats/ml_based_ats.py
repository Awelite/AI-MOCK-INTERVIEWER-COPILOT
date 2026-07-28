import os
import numpy as np
import joblib

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

# ── Lazy-load state ───────────────────────────────────────────────────────────
# sentence_transformers is NOT imported at module level — importing the library
# alone takes ~15s. Everything is deferred to the first ATS scoring call.
# ─────────────────────────────────────────────────────────────────────────────

_sbert = None
_lgbm_model = None


def _get_models():
    global _sbert, _lgbm_model
    if _sbert is None:
        print("[ats] Loading ATS ML models (lazy)...")
        from sentence_transformers import SentenceTransformer
        _sbert = SentenceTransformer(SBERT_PATH)
        _lgbm_model = joblib.load(LGBM_PATH)
        print("[ats] ATS ML models loaded.")
    return _sbert, _lgbm_model


def run_ml_based_ats(
    resume_text,
    jd_text
):
    sbert, lgbm_model = _get_models()

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