from module8.schemas.interview_schema import (
    CandidateInterview
)

from module8.transformer.semantic_engine import (
    SemanticEngine
)

from module8.rag.knowledge_base import (
    KnowledgeBase
)


class IntelligenceEngine:

    def __init__(self):

        self.semantic_engine = (
            SemanticEngine()
        )

        self.knowledge_base = (
            KnowledgeBase()
        )

        self._load_knowledge()

    def _load_knowledge(self):

        docs = [

            "Normalization removes redundancy in databases",

            "Indexing improves query performance",

            "Python supports object oriented programming",

            "REST APIs use HTTP methods",

            "Database normalization improves consistency",

            "Encapsulation protects object data"
        ]

        self.knowledge_base.add_documents(
            docs
        )

    def evaluate_technical_answer(
        self,
        expected_answer,
        user_answer
    ):

        retrieved_knowledge = (
            self.knowledge_base.search(
                user_answer
            )
        )

        semantic_score = (
            self.semantic_engine.compare_answers(
                expected_answer,
                user_answer
            )
        )

        evaluation = {

            "user_answer": user_answer,

            "expected_answer": expected_answer,

            "semantic_score": semantic_score,

            "retrieved_knowledge": (
                retrieved_knowledge
            )
        }

        if semantic_score >= 0.75:

            evaluation[
                "decision"
            ] = "Strong Understanding"

        elif semantic_score >= 0.5:

            evaluation[
                "decision"
            ] = "Partial Understanding"

        else:

            evaluation[
                "decision"
            ] = "Weak Understanding"

        return evaluation

    def evaluate_candidate(
        self,
        candidate: CandidateInterview
    ):

        technical_results = []

        for answer in candidate.technical:

            result = (
                self.evaluate_technical_answer(
                    answer.expected_answer,
                    answer.user_answer
                )
            )

            technical_results.append(
                result
            )

        return {

            "candidate_id":
            candidate.candidate_id,

            "technical_evaluation":
            technical_results
        }