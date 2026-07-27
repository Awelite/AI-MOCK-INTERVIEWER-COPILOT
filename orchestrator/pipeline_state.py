class PipelineState:

    def __init__(self):

        # ── CANDIDATE IDENTITY ─────────────────────────
        self.candidate_id = None

        self.resume_path = None

        self.job_description = None

        # ── RESUME / ATS ───────────────────────────────
        self.resume_text = None

        self.ats_result = None

        self.final_ats_score = 0.0

        # ── QUESTION GENERATION ────────────────────────
        self.generated_questions = None

        # Candidate's written answers to generated Qs
        self.qgen_answers = []

        # ── ASSESSMENT PLANNING ────────────────────────
        self.assessment_plan = None

        # ── CODING ROUND ───────────────────────────────
        self.selected_problem = None

        self.next_problem = None

        self.coding_result = None

        self.next_coding_difficulty = None

        self.coding_session = None

        self.coding_questions = 1

        self.final_coding_score = 0

        self.coding_scores = []

        self.attempted_problems = []

        self.coding_report = None

        # ── APTITUDE ROUND ─────────────────────────────
        self.aptitude_question_count = 10

        self.aptitude_result = None

        self.final_aptitude_score = 0

        self.aptitude_report = None

        # ── HR ROUND ───────────────────────────────────

        # Questions selected during GET /hr/questions
        self.hr_session_questions = []

        self.hr_results = []

        self.final_hr_score = 0

        self.hr_report = None

        # ── SEMANTIC SCORE (from QGEN answers) ─────────
        # Computed in run_qgen_answers_semantic_phase()
        # Used by Module8 instead of hardcoded 75
        self.final_semantic_score = 0.0

        # ── MODULE8 / FINAL ────────────────────────────
        self.module8_result = None

        self.technical_result = None

        self.final_output = None

        self.final_decision = None
