import json
import os
from datetime import datetime


class MemoryEngine:

    def __init__(self):

        self.memory_file = (
            "module8/memory/interview_memory.json"
        )

        if not os.path.exists(
            self.memory_file
        ):

            with open(
                self.memory_file,
                "w"
            ) as f:

                json.dump([], f)

    # ---------------------------------
    # SAVE INTERVIEW
    # ---------------------------------

    def save_interview(
        self,
        candidate_id,
        pipeline_result,
        advanced_feedback
    ):

        with open(
            self.memory_file,
            "r"
        ) as f:

            data = json.load(f)

        interview_record = {

            "candidate_id":
                candidate_id,

            "timestamp":
                str(datetime.now()),

            "overall_score":
                pipeline_result[
                    "overall_score"
                ],

            "difficulty":
                pipeline_result[
                    "difficulty"
                ],

            "recommendation":
                pipeline_result[
                    "recommendation"
                ],

            "advanced_feedback":
                advanced_feedback
        }

        data.append(
            interview_record
        )

        with open(
            self.memory_file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

        return (
            "Interview saved successfully"
        )

    # ---------------------------------
    # GET HISTORY
    # ---------------------------------

    def get_candidate_history(
        self,
        candidate_id
    ):

        with open(
            self.memory_file,
            "r"
        ) as f:

            data = json.load(f)

        history = []

        for record in data:

            if (
                record["candidate_id"]
                ==
                candidate_id
            ):

                history.append(record)

        return history