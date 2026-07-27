import csv
import random
import time


class MCQEngine:

    def __init__(self, question_files):

        if isinstance(question_files, str):
            question_files = [question_files]

        self.question_files = question_files
        self.question_bank = []
        self.selected_questions = []
        self.user_answers = {}

        self.start_time = None
        self.duration = None
        self.completed = False

        self._load_questions()

    # -------------------------
    # LOAD QUESTIONS
    # -------------------------
    def _load_questions(self):

        for file_path in self.question_files:

            with open(file_path, mode='r', encoding='utf-8') as file:

                reader = csv.DictReader(file)

                for row in reader:

                    self.question_bank.append({

                        "id": f"{file_path}_{row.get('id')}",

                        "question": row.get("question"),

                        "option_a": row.get("option_a"),
                        "option_b": row.get("option_b"),
                        "option_c": row.get("option_c"),
                        "option_d": row.get("option_d"),

                        "correct_option": row.get("correct_option")

                    })

    # -------------------------
    # START TEST
    # -------------------------
    def start_test(self, total_questions=5, duration_seconds=180):

        if total_questions > len(self.question_bank):
            raise ValueError(
                "Not enough questions available."
            )

        self.selected_questions = random.sample(
            self.question_bank,
            total_questions
        )

        self.user_answers = {}

        self.start_time = time.time()

        self.duration = duration_seconds

        self.completed = False

    # -------------------------
    # GET QUESTION
    # -------------------------
    def get_question(self, index):

        if index >= len(self.selected_questions):
            return None

        return self.selected_questions[index]

    # -------------------------
    # SUBMIT ANSWER
    # -------------------------
    def submit_answer(self, question_id, selected_option):

        self.user_answers[str(question_id)] = (
            selected_option.upper()
        )

    # -------------------------
    # TIME CHECK
    # -------------------------
    def is_time_up(self):

        if self.start_time is None:
            return False

        elapsed = time.time() - self.start_time

        return elapsed >= self.duration

    # -------------------------
    # REMAINING TIME
    # -------------------------
    def get_remaining_time(self):

        if self.start_time is None:
            return self.duration

        remaining = self.duration - (
            time.time() - self.start_time
        )

        return max(0, int(remaining))

    # -------------------------
    # CALCULATE SCORE
    # -------------------------
    def calculate_score(self):

        correct = 0

        total = len(self.selected_questions)

        for question in self.selected_questions:

            qid = question["id"]

            correct_option = (
                question["correct_option"].upper()
            )

            user_answer = self.user_answers.get(qid)

            if user_answer == correct_option:
                correct += 1

        incorrect = total - correct

        accuracy = (
            (correct / total) * 100
            if total > 0 else 0
        )

        self.completed = True

        return {

            "total_questions": total,

            "correct": correct,

            "incorrect": incorrect,

            "accuracy_percent": round(
                accuracy,
                2
            )
        }