from qgen.qgen_engine import (
    tokenizer_1,
    model_1
)

prompt = """
Generate 5 backend interview questions.

Skills:
Python
SQL
Docker
FastAPI

Difficulty:
medium
"""

inputs = tokenizer_1(
    prompt,
    return_tensors="pt"
)

outputs = model_1.generate(
    **inputs,
    max_new_tokens=200
)

print(
    tokenizer_1.decode(
        outputs[0],
        skip_special_tokens=True
    )
)