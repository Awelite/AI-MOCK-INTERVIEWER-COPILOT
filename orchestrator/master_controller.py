from orchestrator.pipeline_state import (
    PipelineState
)

from orchestrator.module_registry import (
    ModuleRegistry
)

from module8.transformer.semantic_engine import (
    SemanticEngine
)


class MasterController:

    def __init__(self):

        self.state = PipelineState()

        self.registry = ModuleRegistry()

        # SemanticEngine is a heavy model load —
        # initialise once per controller instance.
        self.semantic_engine = SemanticEngine()

    # ─────────────────────────────────────────────────
    # INITIALIZE
    # ─────────────────────────────────────────────────

    def initialize_candidate(
        self,
        candidate_id,
        resume_path,
        job_description,
        coding_questions=1,
        aptitude_questions=10
    ):

        self.state.candidate_id = (
            candidate_id
        )

        self.state.resume_path = (
            resume_path
        )

        self.state.job_description = (
            job_description
        )

        self.state.coding_questions = (
            coding_questions
        )

        self.state.coding_session = (

            self.registry
            .coding_session_manager(

                total_questions=coding_questions
            )
        )

        self.state.aptitude_question_count = (
            aptitude_questions
        )

        print(
            "Candidate initialized."
        )

    # ─────────────────────────────────────────────────
    # STEP 1 — ATS
    # ─────────────────────────────────────────────────

    def run_ats_phase(self):

        print(
            "\nSTEP 1 — ATS ANALYSIS"
        )

        resume_text = (
            self.registry.resume_loader(
                self.state.resume_path
            )
        )

        self.state.resume_text = (
            resume_text
        )

        ats_result = (
            self.registry.ats_engine(
                resume_text,
                self.state.job_description
            )
        )

        self.state.ats_result = (
            ats_result
        )

        self.state.final_ats_score = ats_result.get("ats_score", 0.0)

        print(
            ats_result
        )

    # ─────────────────────────────────────────────────
    # STEP 2 — QUESTION GENERATION
    # ─────────────────────────────────────────────────

    def run_qgen_phase(self):

        print(
            "\nSTEP 2 — QUESTION GENERATION"
        )

        ats_result = (
            self.state.ats_result
        )

        questions = (
            self.registry.qgen_engine
            .generate_questions(
                ats_result
            )
        )

        self.state.generated_questions = (
            questions
        )

        print(
            questions
        )

    # ─────────────────────────────────────────────────
    # STEP 2B — SEMANTIC SCORING OF QGEN ANSWERS
    # Called after candidate submits QGEN answers.
    # Compares each candidate answer against its
    # corresponding generated question text as a
    # reference signal.
    # ─────────────────────────────────────────────────

    def run_qgen_semantic_phase(self):

        print(
            "\nSTEP 2B — QGEN SEMANTIC SCORING"
        )

        questions = (
            self.state
            .generated_questions
            .get("questions", [])
        )

        answers = (
            self.state.qgen_answers
        )

        if not questions or not answers:

            # Default to neutral score if
            # no answers were submitted.
            self.state.final_semantic_score = 50.0

            print(
                "No QGEN answers — "
                "semantic score defaulted to 50.0"
            )

            return

        scores = []

        for question, answer in zip(
            questions,
            answers
        ):

            if not answer or not answer.strip():
                continue

            similarity = (
                self.semantic_engine
                .compare_answers(
                    question,
                    answer
                )
            )

            # Convert 0-1 cosine to 0-100
            scores.append(
                round(similarity * 100, 2)
            )

        if scores:

            avg = round(
                sum(scores) / len(scores),
                2
            )

        else:

            avg = 50.0

        self.state.final_semantic_score = avg

        print(
            f"Semantic Score (QGEN): {avg}"
        )

    # ─────────────────────────────────────────────────
    # STEP 3 — ASSESSMENT PLANNING
    # ─────────────────────────────────────────────────

    def run_assessment_planning_phase(
        self
    ):

        print(
            "\nSTEP 3 — ASSESSMENT PLANNING"
        )

        plan = (

            self.registry
            .assessment_planner
            .recommend_assessment(

                self.state.ats_result,

                self.state.job_description
            )
        )

        self.state.assessment_plan = (
            plan
        )

        print(plan)

    # ─────────────────────────────────────────────────
    # STEP 4 — PROBLEM SELECTION
    # ─────────────────────────────────────────────────

    def run_problem_selection_phase(
    self
    ):

        print(
            "\nSTEP 4 — PROBLEM SELECTION"
        )

        plan = (
            self.state.assessment_plan
        )

        problem = (

            self.registry
            .problem_selector
            .select_problem(

                topic=plan["topic"],

                difficulty=plan["difficulty"]
            )
        )

        self.state.selected_problem = (
            problem
        )

        print(problem)

    # ─────────────────────────────────────────────────
    # STEP 5 — CODING PHASE (single problem)
    # ─────────────────────────────────────────────────

    def run_coding_phase(

            self,

            candidate_code

        ):

        print(
            "\nSTEP 5 — CODING ROUND"
        )

        problem = (
            self.state.selected_problem
        )

        print(
            f"Selected: {problem['title']}"
        )

        result = (

            self.registry
            .coding_engine
            .evaluate_submission(

                problem,

                candidate_code,

                "python"
            )
        )

        self.state.coding_result = (
            result
        )

        self.state.coding_session.add_score(

            result["score"]
        )

        self.state.coding_scores.append(

            result["score"]

        )

        self.state.attempted_problems.append(

            problem["id"]

        )

        self.state.final_coding_score = (

            self.state
            .coding_session
            .final_score()
        )

        print(result)

        print(

            f"Current Session Score: "
            f"{self.state.final_coding_score}"
        )

        self.registry.attempt_repository.save_attempt(

            user_id=self.state.candidate_id,

            problem_id=problem["id"],

            language="python",

            code=candidate_code,
            passed_tests=result["passed"],

            total_tests=result["total"],

            score=result["score"]
        )

        print(
            "Attempt Saved To Database"
        )

    # ─────────────────────────────────────────────────
    # STEP 5 LOOP — CODING SESSION (multi-problem)
    # ─────────────────────────────────────────────────

    def run_coding_session_phase(

        self,

        candidate_code

    ):

        session = (
            self.state.coding_session
        )

        while not session.is_finished():

            self.run_coding_phase(
                candidate_code
            )

            if not session.is_finished():

                self.run_adaptive_coding_phase()

                self.run_next_problem_phase()

                self.state.selected_problem = (
                    self.state.next_problem
                )

        self.state.final_coding_score = (

            session.final_score()

        )

        print(

            "\nFINAL CODING SCORE:",

            self.state.final_coding_score

        )

    # ─────────────────────────────────────────────────
    # STEP 6 — ADAPTIVE DIFFICULTY
    # ─────────────────────────────────────────────────

    def run_adaptive_coding_phase(

        self

    ):

        print(
            "\nSTEP 6 — ADAPTIVE CODING"
        )

        score = (
            self.state.coding_result[
                "score"
            ]
        )

        difficulty = (

            self.registry
            .difficulty_controller
            .adjust_difficulty(
                score
            )
        )

        self.state.next_coding_difficulty = (
            difficulty
        )

        print(

            f"Next Coding Difficulty: "
            f"{difficulty}"
        )

    # ─────────────────────────────────────────────────
    # STEP 7 — NEXT PROBLEM
    # ─────────────────────────────────────────────────

    def run_next_problem_phase(

        self

    ):

        print(
            "\nSTEP 7 — NEXT PROBLEM"
        )

        current_topic = (

            self.state.selected_problem[
                "topic"
            ]
        )

        difficulty = (

            self.state.next_coding_difficulty
        )

        next_problem = (

            self.registry
            .problem_selector
            .select_problem(

                topic=current_topic,

                difficulty=difficulty,
                
                exclude_ids=self.state.attempted_problems
            )
        )

        self.state.next_problem = (
            next_problem
        )

        print(next_problem)

    # ─────────────────────────────────────────────────
    # STEP 8 — CODING REPORT
    # ─────────────────────────────────────────────────

    def run_coding_report_phase(

        self

    ):

        print(

            "\nSTEP 8 — CODING REPORT"

        )

        report = (

            self.registry
            .coding_report
            .generate(

                self.state.coding_scores,

                self.state.attempted_problems

            )
        )

        self.state.coding_report = (
            report
        )

        print(report)

    # ─────────────────────────────────────────────────
    # STEP 9 — APTITUDE
    # ─────────────────────────────────────────────────

    def run_aptitude_phase(self):

        print(
            "\nSTEP 9 — APTITUDE ROUND"
        )

        engine = (
            self.registry.aptitude_engine
        )

        engine.start_test(
            total_questions=
            self.state.aptitude_question_count

        )

        # dummy answers for testing

        for q in engine.selected_questions:

            engine.submit_answer(
                q["id"],
                q["correct_option"]
            )

        result = (
            engine.calculate_score()
        )

        self.state.aptitude_result = (
            result
        )

        self.state.final_aptitude_score = (

            result[
                "accuracy_percent"
            ]
        )

        print(result)

        self.registry.aptitude_repository.save_attempt(

            self.state.candidate_id,

            result

        )

    # ─────────────────────────────────────────────────
    # STEP 10 — HR ROUND
    # ─────────────────────────────────────────────────

    def run_hr_phase(

        self

    ):

        print(

            "\nSTEP 10 — HR ROUND"

        )

        sample_answers = [

            "I led a team project and achieved success.",

            "I built backend systems using Python.",

            "I handle pressure by planning tasks."
        ]

        results = (

            self.registry
            .hr_engine
            .conduct_round(

                sample_answers
            )
        )

        self.state.hr_results = (
            results
        )

        scores = [

            r["evaluation"][
                "hr_score"
            ]

            for r in results
        ]

        self.state.final_hr_score = (

            round(

                sum(scores)

                /

                len(scores),

                2
            )
        )

        print(results)

    # ─────────────────────────────────────────────────
    # STEP 11 — HR REPORT
    # ─────────────────────────────────────────────────

    def run_hr_report_phase(

        self

    ):

        print(

            "\nSTEP 11 — HR REPORT"

        )

        report = (

            self.registry
            .hr_report
            .generate(

                self.state.hr_results
            )
        )

        self.state.hr_report = (
            report
        )

        print(report)

    # ─────────────────────────────────────────────────
    # FINAL — MODULE8 DECISION
    # Uses real final_semantic_score (not hardcoded 75)
    # ─────────────────────────────────────────────────

    def run_module8_phase(self):

        print(
            "\nSTEP FINAL — MODULE8 DECISION"
        )

        ats_score = (
            self.state.final_ats_score
        )

        coding_score = (
            self.state.final_coding_score
        )

        aptitude_score = (
            self.state.final_aptitude_score
        )

        # Real semantic score from QGEN answers
        semantic_score = (
            self.state.final_semantic_score
        )

        hr_score = (
            self.state.final_hr_score
        )

        level = (

            self.registry
            .module8_engine
            .evaluate_candidate_level(

                ats_score,

                coding_score,

                aptitude_score,

                semantic_score,

                hr_score

            )
        )

        next_round = (

            self.registry
            .module8_engine
            .next_round(
                level
            )
        )

        result = {

            "level": level,

            "next_round":
            next_round.value
        }

        self.state.module8_result = (
            result
        )

        print(result)

    # ─────────────────────────────────────────────────
    # FULL PIPELINE (legacy / CLI usage)
    # ─────────────────────────────────────────────────

    def run_pipeline(

            self,

            candidate_code

        ):

        print(
            "\nMASTER INTERVIEW PIPELINE STARTED"
        )

        print(
            f"Candidate: {self.state.candidate_id}"
        )

        self.run_ats_phase()

        self.run_qgen_phase()

        self.run_assessment_planning_phase()

        self.run_problem_selection_phase()

        self.run_coding_session_phase(
            candidate_code
        )

        self.run_coding_report_phase()
        self.run_aptitude_phase()
        self.run_hr_phase()

        self.run_hr_report_phase()
        self.run_module8_phase()