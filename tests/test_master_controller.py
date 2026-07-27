from orchestrator.master_controller import (
    MasterController
)

controller = MasterController()

controller.initialize_candidate(

    candidate_id="CAND_001",

    resume_path="uploads/resume.pdf",

    job_description=(
        "Backend Developer with Python SQL APIs Docker"
    ),

    coding_questions=3
)

controller.run_pipeline(
"""
print("grouped")
"""
)