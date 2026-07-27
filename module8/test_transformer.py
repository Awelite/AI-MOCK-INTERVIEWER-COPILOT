from module8.transformer.semantic_engine import SemanticEngine


engine = SemanticEngine()

expected = "Normalization removes redundancy"

user = "Normalization reduces duplicate data"


score = engine.compare_answers(
    expected,
    user
)

print("\nSemantic Similarity Score:")
print(score)