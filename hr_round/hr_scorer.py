from hr_round.sentiment_model import (
    sentiment_score
)

from hr_round.confidence_model import (
    confidence_score
)

from hr_round.clarity_model import (
    clarity_score
)

from hr_round.structure_model import (
    structure_score
)

from module8.transformer.semantic_engine import (
    SemanticEngine
)

import hr_round.feedback_generator as fg

# Lazy-loaded — the transformer model is only initialised the first time
# an HR answer is evaluated, not at import time.
_semantic_engine = None

def _get_semantic_engine():
    global _semantic_engine
    if _semantic_engine is None:
        print("[hr_scorer] Loading SemanticEngine (lazy)...")
        _semantic_engine = SemanticEngine()
    return _semantic_engine

def evaluate_answer(
    text,
    ideal_answer=""
):
    if len(text.strip()) < 20:
        return {
            "semantic_score": 0,
            "positivity": 0,
            "confidence": 0,
            "clarity": 0,
            "structure": 0,
            "hr_score": 0,
            "feedback": "Answer is too short. Please provide a more detailed response."
        }

    semantic = 0

    if ideal_answer:
        semantic = (
            _get_semantic_engine()
            .compare_answers(
                ideal_answer,
                text
            )
        )

    p = sentiment_score(text)
    c = confidence_score(text)
    cl = clarity_score(text)
    # Normalize features
    semantic_norm = min(semantic * 2.5, 1.0)
    p_norm = min(p * 1.5, 1.0)
    c_norm = min(c * 1.5, 1.0)
    cl_norm = min(cl * 1.5, 1.0)
    
    # Structure based on length/words since STAR words are too rigid
    words = len(text.split())
    if words > 30:
        s_norm = 1.0
    elif words > 15:
        s_norm = 0.5
    else:
        s_norm = 0.0

    hr_score = (
        semantic_norm * 0.15 +
        p_norm * 0.15 +
        c_norm * 0.25 +
        cl_norm * 0.20 +
        s_norm * 0.25
    ) * 100

    # Penalize if the semantic relevance is extremely low (Task 3)
    if semantic_norm < 0.2:
        hr_score = min(hr_score, 15.0)

    feedback = fg.generate_feedback(p,c,cl,s_norm)

    return {

        "semantic_score":
        round(
            semantic * 100,
            2
        ),

        "positivity": round(p,2),
        "confidence": round(c,2),
        "clarity": round(cl,2),
        "structure": round(s_norm,2),
        "hr_score": round(hr_score,2),
        "feedback": feedback
    }