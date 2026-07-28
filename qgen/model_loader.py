import os

BASE_DIR = os.path.dirname(__file__)

MODEL_1_PATH = os.path.join(
    BASE_DIR,
    "models",
    "flan_t5_qgen_ep6"
)

MODEL_2_PATH = os.path.join(
    BASE_DIR,
    "models",
    "flan_t5_qgen_ep6_clean"
)

# ── Lazy-load state ───────────────────────────────────────────────────────────
# Nothing is loaded at import time — not even the `transformers` library.
# Both models are loaded on the first call to get_models().
# ─────────────────────────────────────────────────────────────────────────────

_tokenizer_1 = None
_model_1     = None
_tokenizer_2 = None
_model_2     = None


def get_models():
    """Return (tokenizer_1, model_1, tokenizer_2, model_2), loading on first call."""
    global _tokenizer_1, _model_1, _tokenizer_2, _model_2

    if _model_1 is None:
        print("[qgen] Loading QGEN Models (lazy)...")
        # Import transformers lazily — importing the library itself is slow (~15s)
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        _tokenizer_1 = AutoTokenizer.from_pretrained(MODEL_1_PATH)
        _model_1     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_1_PATH)

        _tokenizer_2 = AutoTokenizer.from_pretrained(MODEL_2_PATH)
        _model_2     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_2_PATH)

        print("[qgen] QGEN Models Loaded.")

    return _tokenizer_1, _model_1, _tokenizer_2, _model_2


# ── Backward-compat shim ──────────────────────────────────────────────────────
# Any module that does `from qgen.model_loader import tokenizer_1, model_1 …`
# will get proxy objects that load the real models on first attribute access.
# ─────────────────────────────────────────────────────────────────────────────

class _LazyModel:
    """Thin proxy: delegates all attribute access to the real loaded model."""

    def __init__(self, index: int):
        self._index = index
        self._real  = None

    def _load(self):
        if self._real is None:
            self._real = get_models()[self._index]
        return self._real

    def __getattr__(self, name):
        return getattr(self._load(), name)

    def __call__(self, *args, **kwargs):
        return self._load()(*args, **kwargs)


tokenizer_1 = _LazyModel(0)
model_1     = _LazyModel(1)
tokenizer_2 = _LazyModel(2)
model_2     = _LazyModel(3)