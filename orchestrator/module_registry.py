from ats.extract_text import (
    load_text
)

from ats.hybrid_ats_pipeline import (
    run_ats_pipeline
)

from qgen.qgen_engine import (
    QGenEngine
)

from module8.core.assessment_planner import (
    AssessmentPlanner
)

from coding_round.problem_selector import (
    ProblemSelector
)

from coding_round.coding_engine import (
    CodingEngine
)

from module8.orchestrator.interview_orchestrator import (
    InterviewOrchestrator
)

from coding_round.attempt_repository import (
    AttemptRepository
)

from module8.orchestrator.difficulty_controller import (
    DifficultyController
)

from coding_round.coding_session_manager import (
    CodingSessionManager
)

from coding_round.final_report import (
    CodingFinalReport
)

from aptitude_round.aptitude_engine import (
    MCQEngine
)

from aptitude_round.final_report import (
    AptitudeReportGenerator
)

from aptitude_round.aptitude_repository import (
    AptitudeRepository
)

from hr_round.hr_engine import (
    HREngine
)

from hr_round.hr_report import (
    HRReport
)


class ModuleRegistry:

    def __init__(self):

        self.resume_loader = (
            load_text
        )

        self.ats_engine = (
            run_ats_pipeline
        )

        self.qgen_engine = (
            QGenEngine()
        )

        self.assessment_planner = (
            AssessmentPlanner()
        )

        self.problem_selector = (
            ProblemSelector()
        )

        self.coding_engine = (
            CodingEngine()
        )

        self.hr_engine = None

        self.module8_engine = (
            InterviewOrchestrator()
        )

        self.attempt_repository = (
            AttemptRepository()
        )

        self.difficulty_controller = (
            DifficultyController()
        )

        self.coding_session_manager = (
            CodingSessionManager
        )

        self.coding_report = (
            CodingFinalReport()
        )

        self.aptitude_engine = MCQEngine(
            [
                "aptitude_round/datasets/MNC_Aptitude_Questions.csv",
                "aptitude_round/datasets/Logical_Reasoning_Questions.csv"
            ]
        )

        self.aptitude_report_generator = (

            AptitudeReportGenerator()
        )

        self.aptitude_repository = (
            AptitudeRepository()
        )

        self.hr_engine = (
            HREngine()
        )

        self.hr_report = (
            HRReport()
        )