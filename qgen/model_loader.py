import os

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


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


print(
    "Loading QGEN Models..."
)


tokenizer_1 = AutoTokenizer.from_pretrained(
    MODEL_1_PATH
)

model_1 = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_1_PATH
)


tokenizer_2 = AutoTokenizer.from_pretrained(
    MODEL_2_PATH
)

model_2 = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_2_PATH
)


print(
    "QGEN Models Loaded."
)