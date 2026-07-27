from module8.core.intelligence_engine import (
    IntelligenceEngine
)

from module8.transformer.semantic_engine import (
    SemanticEngine
)

from module8.rag.rag_engine import (
    RAGEngine
)

from module8.orchestrator.difficulty_controller import (
    DifficultyController
)

from module8.orchestrator.transition_manager import (
    TransitionManager
)


class MasterPipeline:

    def __init__(self):

        self.intelligence_engine = (
            IntelligenceEngine()
        )

        self.semantic_engine = (
            SemanticEngine()
        )

        self.rag_engine = (
            RAGEngine()
        )

        self.difficulty_controller = (
            DifficultyController()
        )

        self.transition_manager = (
            TransitionManager()
        )

    def run_pipeline(
        self,
        candidate_data
    ):

        print("\nSTEP 1 — Intelligence Evaluation")

        intelligence_result = (
            self.intelligence_engine
            .evaluate_candidate(
                candidate_data
            )
        )

        print(intelligence_result)

        print("\nSTEP 2 — Semantic Evaluation")

        semantic_score = (
            self.semantic_engine
            .compare_answers(
                "Normalization removes redundancy",
                "Normalization reduces duplicate data"
            )
        )

        semantic_percentage = (
            semantic_score * 100
        )

        print(
            f"Semantic Score: "
            f"{semantic_percentage}"
        )

        print("\nSTEP 3 — RAG Retrieval")

        rag_result = (
            self.rag_engine
            .retrieve_knowledge(
                "backend developer"
            )
        )

        print(rag_result)

        print("\nSTEP 4 — Difficulty Control")

        technical_semantic_score = (
            intelligence_result[
                "technical_evaluation"
            ][0]["semantic_score"]
        ) * 100

        difficulty = (
            self.difficulty_controller
            .adjust_difficulty(
                technical_semantic_score
            )
        )

        print(difficulty)

        print("\nSTEP 5 — Transition Decision")

        transition = (
            self.transition_manager
            .decide_transition(

                level=difficulty,

                coding_score=75,

                semantic_score=
                semantic_percentage
            )
        )

        print(transition)

        print("\nSTEP 6 — FINAL DECISION")

        final_result = {

            "candidate":
            candidate_data.candidate_id,

            "overall_score":
            semantic_percentage,

            "difficulty":
            difficulty,

            "transition":
            transition,

            "recommendation":
            "Proceed to Final HR Round"
        }

        return final_result