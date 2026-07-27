"""
api/routes/interview.py
───────────────────────
Session-based interview flow router.

Endpoints (all under /api/v1/interview):
  POST   /start
  POST   /qgen/submit
  GET    /coding/problem/{session_id}
  POST   /coding/submit
  GET    /aptitude/questions/{session_id}
  POST   /aptitude/submit
  GET    /hr/questions/{session_id}
  POST   /hr/submit
  GET    /final/{session_id}
  GET    /status/{session_id}
"""

import uuid
import os
import json
import requests
import base64
import tempfile
import shutil
import time
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ats.resume_analyzer import analyze_resume

from datetime import datetime
from typing import List, Optional

from fastapi import (
    APIRouter,
    File,
    Form,
    UploadFile,
    HTTPException,
)
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from orchestrator.master_controller import (
    MasterController
)

from api.session_store import (
    SESSION_STORE,
    ROUND_INIT,
    ROUND_ATS_DONE,
    ROUND_QGEN,
    ROUND_CODING,
    ROUND_APTITUDE,
    ROUND_HR,
    ROUND_FINAL,
    ROUND_COMPLETE,
    create_session,
    get_session,
    set_round,
)

from coding_round.ai_review import (
    generate_ai_review
)


# ─────────────────────────────────────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────────────────────────────────────

router = APIRouter(
    prefix="/api/v1/interview",
    tags=["Interview Session"]
)


# ─────────────────────────────────────────────────────────────────────────────
# PYDANTIC SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────

class QGenAnswer(BaseModel):
    question_index: int
    answer: str


class QGenSubmitRequest(BaseModel):
    session_id: str
    answers: List[QGenAnswer]


class CodingSubmitRequest(BaseModel):
    session_id: str
    code: str
    language: str = "python"
    problem_slug: str


class AptitudeAnswer(BaseModel):
    question_id: str
    selected_option: str


class AptitudeSubmitRequest(BaseModel):
    session_id: str
    answers: List[AptitudeAnswer]


class HRSubmitRequest(BaseModel):
    session_id: str
    answers: List[str]


# ─────────────────────────────────────────────────────────────────────────────
# JUDGE0 CONFIG (mirrors existing /coding/submit logic)
# ─────────────────────────────────────────────────────────────────────────────

JUDGE0_URL = "http://localhost:2358/submissions?base64_encoded=false&wait=true"

LANGUAGE_MAP = {
    "python": 71,
    "cpp":    54,
}

judge0_session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["POST", "GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
judge0_session.mount("http://", adapter)
judge0_session.mount("https://", adapter)

UPLOADS_DIR = "uploads"


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def require_session(session_id: str) -> dict:
    """
    Fetch a session or raise 404.
    Returns the session entry dict.
    """
    entry = get_session(session_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found. "
                   f"Start with POST /api/v1/interview/start"
        )
    return entry


def require_round(entry: dict, expected: str) -> None:
    """
    Enforce that the session is in the expected round.
    Raises 409 Conflict with a clear message otherwise.
    """
    current = entry["current_round"]
    if current != expected:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Wrong round. Session is at '{current}', "
                f"but this endpoint expects '{expected}'."
            )
        )


def safe_json(value):
    """
    Attempt to JSON-parse a string field (e.g. starter_code from DB).
    Returns original value on failure.
    """
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return value
    return value

import re
def normalize_output(text: str) -> str:
    """Normalize output for comparison: collapse all whitespace, strip trailing, lowercase."""
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")
    text = re.sub(r'[ \t]+', ' ', text)
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = text.strip()
    text = text.replace('"', "'")
    text = text.lower()
    return text


# ─────────────────────────────────────────────────────────────────────────────
# POST /start
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/start")
async def start_interview(
    candidate_id:        str  = Form(...),
    job_description:     str  = Form(...),
    resume_file:         UploadFile = File(...),
    coding_questions:    int  = Form(1),
    aptitude_questions:  int  = Form(10),
):
    """
    Initialize a candidate session.

    1. Save uploaded resume to /uploads/{session_id}/
    2. initialize_candidate() on a fresh MasterController
    3. run_ats_phase()         → ats_result
    4. run_qgen_phase()        → generated_questions
    5. run_assessment_planning_phase() → assessment_plan
    6. Store session in SESSION_STORE
    7. Return session_id + ATS result + questions
    """

    # ── 1. Generate session ID ──────────────────────
    session_id = str(uuid.uuid4())

    # ── 2. Save resume file ─────────────────────────
    session_upload_dir = os.path.join(
        UPLOADS_DIR,
        session_id
    )
    os.makedirs(session_upload_dir, exist_ok=True)

    resume_filename = resume_file.filename or "resume"
    resume_path = os.path.join(
        session_upload_dir,
        resume_filename
    )

    contents = await resume_file.read()
    with open(resume_path, "wb") as f:
        f.write(contents)

    # ── 3. Build MasterController ───────────────────
    controller = MasterController()

    controller.initialize_candidate(
        candidate_id=candidate_id,
        resume_path=resume_path,
        job_description=job_description,
        coding_questions=coding_questions,
        aptitude_questions=aptitude_questions,
    )

    # ── 4. ATS Phase ────────────────────────────────
    try:
        controller.run_ats_phase()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"ATS phase failed: {str(exc)}"
        )

    # ── 5. QGEN Phase ────────────────────────────────
    try:
        controller.run_qgen_phase()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"QGEN phase failed: {str(exc)}"
        )

    # ── 6. Assessment Planning ───────────────────────
    try:
        controller.run_assessment_planning_phase()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Assessment planning failed: {str(exc)}"
        )

    # ── 7. Register session ─────────────────────────
    create_session(
        session_id=session_id,
        controller=controller,
        candidate_id=candidate_id,
        resume_filename=resume_filename,
    )

    set_round(session_id, ROUND_QGEN)

    state = controller.state

    return {
        "session_id":           session_id,
        "candidate_id":         candidate_id,
        "ats_result":           state.ats_result,
        "assessment_plan":      state.assessment_plan,
        "generated_questions":  state.generated_questions,
        "current_round":        ROUND_QGEN,
        "next_round":           ROUND_CODING,
        "message": (
            "Session started. "
            "Answer the generated questions and "
            "POST to /api/v1/interview/qgen/submit"
        ),
    }




# ─────────────────────────────────────────────────────────────────────────────
# POST /qgen/submit
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/qgen/submit")
def submit_qgen_answers(body: QGenSubmitRequest):
    """
    Candidate submits answers to the generated questions.

    1. Validate session + round
    2. Store answers in state.qgen_answers
    3. Run semantic scoring (replaces hardcoded 75)
    4. Run problem selection for coding round
    5. Advance to CODING round
    """

    entry      = require_session(body.session_id)
    require_round(entry, ROUND_QGEN)
    controller = entry["controller"]
    state      = controller.state

    # ── 1. Store answers sorted by question_index ───
    sorted_answers = sorted(
        body.answers,
        key=lambda a: a.question_index
    )
    state.qgen_answers = [a.answer for a in sorted_answers]

    # ── 2. Semantic scoring ─────────────────────────
    try:
        controller.run_qgen_semantic_phase()
    except Exception as exc:
        # Non-fatal — log and continue with default
        print(f"[WARN] Semantic phase error: {exc}")
        state.final_semantic_score = 50.0

    # ── 3. Problem Selection ────────────────────────
    try:
        controller.run_problem_selection_phase()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Problem selection failed: {str(exc)}"
        )

    set_round(body.session_id, ROUND_CODING)

    return {
        "session_id":       body.session_id,
        "accepted":         True,
        "answers_received": len(state.qgen_answers),
        "semantic_score":   state.final_semantic_score,
        "assessment_plan":  state.assessment_plan,
        "current_round":    ROUND_CODING,
        "next_action": (
            f"GET /api/v1/interview/coding/problem"
            f"/{body.session_id}"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# GET /coding/problem/{session_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/coding/problem/{session_id}")
def get_coding_problem(session_id: str):
    """
    Return the pre-selected coding problem for this session.
    Problem was chosen during run_problem_selection_phase()
    (triggered by POST /qgen/submit).
    """

    entry      = require_session(session_id)
    require_round(entry, ROUND_CODING)
    controller = entry["controller"]
    state      = controller.state

    problem = state.selected_problem

    if not problem:
        raise HTTPException(
            status_code=500,
            detail="No problem selected for this session."
        )

    session     = state.coding_session
    q_attempted = session.current_question
    q_total     = session.total_questions

    # Parse JSON fields from MySQL if they came back as strings
    problem_out = dict(problem)
    if "starter_code" in problem_out:
        problem_out["starter_code"] = safe_json(
            problem_out["starter_code"]
        )

    return {
        "session_id":      session_id,
        "problem":         problem_out,
        "question_number": q_attempted + 1,
        "total_questions": q_total,
        "current_round":   ROUND_CODING,
    }


class CodingRunRequest(BaseModel):
    session_id: str
    code: str
    language: str = "python"
    stdin: str = ""

@router.post("/coding/run")
def run_coding_code(body: CodingRunRequest):
    entry = require_session(body.session_id)
    require_round(entry, ROUND_CODING)
    
    language_id = LANGUAGE_MAP.get(body.language)
    if not language_id:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {body.language}")
        
    start_req = time.time()
    try:
        resp = judge0_session.post(
            "http://localhost:2358/submissions?base64_encoded=true&wait=true",
            json={
                "source_code": base64.b64encode(body.code.encode("utf-8")).decode("ascii"),
                "language_id": language_id,
                "stdin": base64.b64encode(body.stdin.encode("utf-8")).decode("ascii") if body.stdin else None,
            },
            timeout=20,
        )
        result = resp.json()
    except Exception as e:
        return {"output": f"Judge0 execution failed: {str(e)}"}
        
    total_time = time.time() - start_req
    exec_time = float(result.get("time", "0.0") or "0.0")
    polling_time = max(0.0, total_time - exec_time)
    print(f"\n[JUDGE0 LATENCY] Run Code - Req: {total_time:.3f}s | Exec: {exec_time:.3f}s | Polling: {polling_time:.3f}s")
        
    stdout = result.get("stdout")
    stderr = result.get("stderr")
    compile_output = result.get("compile_output")
    
    out_str = ""
    if stdout:
        out_str += base64.b64decode(stdout).decode("utf-8")
    if stderr:
        out_str += base64.b64decode(stderr).decode("utf-8")
    if compile_output:
        out_str += base64.b64decode(compile_output).decode("utf-8")
        
    return {"output": out_str.strip() or "No output."}

# ─────────────────────────────────────────────────────────────────────────────
# POST /coding/submit
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/coding/submit")
def submit_coding_solution(body: CodingSubmitRequest):
    """
    Candidate submits code for the current problem.

    1. Validate session + round
    2. Run Judge0 test cases (mirrors existing /coding/submit)
    3. Record score in CodingSessionManager
    4. If session not finished → adaptive + next problem
    5. If session finished → generate report + advance to APTITUDE
    """

    entry      = require_session(body.session_id)
    require_round(entry, ROUND_CODING)
    controller = entry["controller"]
    state      = controller.state

    language_id = LANGUAGE_MAP.get(body.language)
    if not language_id:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {body.language}"
        )

    problem = state.selected_problem
    if not problem:
        raise HTTPException(
            status_code=500,
            detail="No problem selected. Call /qgen/submit first."
        )

    problem_id   = problem["id"]
    problem_desc = problem.get("description", "")

    # ── 1. Fetch test cases from MySQL ──────────────
    from coding_round.database import get_db as get_mysql_db

    conn   = get_mysql_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT input_data, expected_output, is_hidden
        FROM test_cases
        WHERE problem_id=%s
        """,
        (problem_id,)
    )
    test_cases = cursor.fetchall()
    cursor.close()
    conn.close()

    if not test_cases:
        raise HTTPException(
            status_code=404,
            detail=f"No test cases found for problem_id={problem_id}"
        )

    # ── 2. Run each test case through Judge0 ────────
    results = []
    passed  = 0

    def evaluate_test(test):
        stdin = test["input_data"]
        start_req = time.time()
        try:
            resp = judge0_session.post(
                JUDGE0_URL,
                json={
                    "source_code": body.code,
                    "language_id": language_id,
                    "stdin":       stdin,
                },
                timeout=20,
            )
            result = resp.json()
        except Exception:
            result = {"stderr": "Judge0 unreachable"}
            
        total_time = time.time() - start_req
        exec_time = float(result.get("time", "0.0") or "0.0")
        polling_time = max(0.0, total_time - exec_time)
        print(f"[JUDGE0 LATENCY] Submit Test - Req: {total_time:.3f}s | Exec: {exec_time:.3f}s | Polling: {polling_time:.3f}s")
        return test, result

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(evaluate_test, test): test for test in test_cases}
        
        for future in concurrent.futures.as_completed(futures):
            test, result = future.result()
            
            status      = result.get("status", {})
            status_desc = status.get("description", "Unknown Error")

            stdout         = result.get("stdout") or ""
            stderr         = result.get("stderr") or ""
            compile_output = result.get("compile_output") or ""

            actual_output = (
                stdout.strip()
                or stderr.strip()
                or compile_output.strip()
            )

            expected_output = test["expected_output"].strip()

            act_norm = normalize_output(actual_output)
            exp_norm = normalize_output(expected_output)

            if status_desc == "Accepted" and act_norm == exp_norm:
                verdict   = "Accepted"
                is_passed = True
                passed   += 1
            elif "Compilation Error" in status_desc:
                verdict   = "Compilation Error"
                is_passed = False
            elif "Runtime Error" in status_desc:
                verdict   = "Runtime Error"
                is_passed = False
            elif "Time Limit" in status_desc:
                verdict   = "Time Limit Exceeded"
                is_passed = False
            elif "Memory Limit" in status_desc:
                verdict   = "Memory Limit Exceeded"
                is_passed = False
            else:
                verdict   = "Wrong Answer"
                is_passed = False

            if not test["is_hidden"]:
                results.append({
                    "input":    test["input_data"],
                    "expected": expected_output,
                    "actual":   actual_output,
                    "passed":   is_passed,
                    "verdict":  verdict,
                })

    total = len(test_cases)
    score = round((passed / total) * 100, 2) if total else 0.0

    # ── Overall verdict ──────────────────────────────
    if passed == total:
        overall_verdict = "Accepted"
    elif passed == 0:
        first_v = results[0]["verdict"] if results else "Wrong Answer"
        overall_verdict = first_v
    else:
        overall_verdict = "Partially Accepted"

    # ── AI Review ────────────────────────────────────
    try:
        ai_review = generate_ai_review(
            problem_desc,
            body.code,
            overall_verdict
        )
    except Exception:
        ai_review = "AI review unavailable."

    # ── 3. Record score in MasterController state ───
    state.coding_result = {
        "score":  score,
        "passed": passed,
        "total":  total,
    }
    state.coding_session.add_score(score)
    state.coding_scores.append(score)
    state.attempted_problems.append(problem_id)
    state.final_coding_score = state.coding_session.final_score()

    # Save attempt to DB with real candidate_id
    try:
        controller.registry.attempt_repository.save_attempt(
            user_id=state.candidate_id,
            problem_id=problem_id,
            language=body.language,
            code=body.code,
            passed_tests=passed,
            total_tests=total,
            score=score,
        )
    except Exception as exc:
        print(f"[WARN] save_attempt failed: {exc}")

    session_obj = state.coding_session

    # ── 4. Multi-problem adaptive flow ──────────────
    if not session_obj.is_finished():
        # Adapt difficulty and select next problem
        try:
            controller.run_adaptive_coding_phase()
            controller.run_next_problem_phase()
            state.selected_problem = state.next_problem
        except Exception as exc:
            print(f"[WARN] Adaptive phase: {exc}")

        next_problem_out = dict(state.selected_problem or {})
        if "starter_code" in next_problem_out:
            next_problem_out["starter_code"] = safe_json(
                next_problem_out["starter_code"]
            )

        return {
            "session_id":      body.session_id,
            "verdict":         overall_verdict,
            "passed_tests":    passed,
            "total_tests":     total,
            "score":           score,
            "ai_review":       ai_review,
            "results":         results,
            "coding_session": {
                "questions_attempted": session_obj.current_question,
                "questions_total":     session_obj.total_questions,
                "session_complete":    False,
                "current_score":       state.final_coding_score,
            },
            "next_problem":  next_problem_out,
            "current_round": ROUND_CODING,
            "next_action": (
                f"Submit next problem to "
                f"POST /api/v1/interview/coding/submit"
            ),
        }

    # ── 5. Session complete → generate report ────────
    state.final_coding_score = session_obj.final_score()

    try:
        controller.run_coding_report_phase()
    except Exception as exc:
        print(f"[WARN] Coding report: {exc}")

    set_round(body.session_id, ROUND_APTITUDE)

    response_dict = {
        "session_id":   body.session_id,
        "verdict":      overall_verdict,
        "passed_tests": passed,
        "total_tests":  total,
        "score":        score,
        "ai_review":    ai_review,
        "results":      results,
        "coding_session": {
            "questions_attempted": session_obj.current_question,
            "questions_total":     session_obj.total_questions,
            "session_complete":    True,
            "final_coding_score":  state.final_coding_score,
        },
        "coding_report": state.coding_report,
        "current_round": ROUND_APTITUDE,
        "next_action": (
            f"GET /api/v1/interview/aptitude/questions"
            f"/{body.session_id}"
        ),
    }

    print(f"\n[TRACE] POST /coding/submit ended. session: {body.session_id}, final_coding_score: {state.final_coding_score}")
    return response_dict


# ─────────────────────────────────────────────────────────────────────────────
# GET /aptitude/questions/{session_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/aptitude/questions/{session_id}")
def get_aptitude_questions(session_id: str):
    """
    Start the aptitude test and return all MCQ questions.
    Correct options are NEVER included in the response.
    """

    entry      = require_session(session_id)
    require_round(entry, ROUND_APTITUDE)
    controller = entry["controller"]
    state      = controller.state

    engine = controller.registry.aptitude_engine

    try:
        engine.start_test(
            total_questions=state.aptitude_question_count,
            duration_seconds=300,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not start aptitude test: {str(exc)}"
        )

    # Serve questions WITHOUT correct_option
    questions_out = []
    for q in engine.selected_questions:
        questions_out.append({
            "id":       q["id"],
            "question": q["question"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
        })

    return {
        "session_id":       session_id,
        "total_questions":  state.aptitude_question_count,
        "duration_seconds": 300,
        "questions":        questions_out,
        "current_round":    ROUND_APTITUDE,
    }


# ─────────────────────────────────────────────────────────────────────────────
# POST /aptitude/submit
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/aptitude/submit")
def submit_aptitude_answers(body: AptitudeSubmitRequest):
    """
    Candidate submits MCQ answers.

    1. Submit each answer to MCQEngine
    2. Calculate score
    3. Save to DB via AptitudeRepository
    4. Advance to HR round
    """

    entry      = require_session(body.session_id)
    require_round(entry, ROUND_APTITUDE)
    controller = entry["controller"]
    state      = controller.state
    engine     = controller.registry.aptitude_engine

    # ── 1. Submit answers ────────────────────────────
    for ans in body.answers:
        engine.submit_answer(
            ans.question_id,
            ans.selected_option,
        )

    # ── 2. Calculate score ───────────────────────────
    try:
        result = engine.calculate_score()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Score calculation failed: {str(exc)}"
        )

    state.aptitude_result       = result
    state.final_aptitude_score  = result["accuracy_percent"]

    # ── 3. Save to DB ────────────────────────────────
    try:
        controller.registry.aptitude_repository.save_attempt(
            state.candidate_id,
            result,
        )
    except Exception as exc:
        print(f"[WARN] aptitude_repository.save_attempt: {exc}")

    set_round(body.session_id, ROUND_HR)

    return {
        "session_id":      body.session_id,
        "aptitude_result": result,
        "current_round":   ROUND_HR,
        "next_action": (
            f"GET /api/v1/interview/hr/questions"
            f"/{body.session_id}"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# GET /hr/questions/{session_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/hr/questions/{session_id}")
def get_hr_questions(
    session_id: str,
    count: int = 3,
):
    """
    Select and return HR questions for this session.
    Uses the new HREngine.get_questions(count) method.
    Questions are persisted in state.hr_session_questions
    so that POST /hr/submit can evaluate against the same set.
    """

    entry      = require_session(session_id)
    require_round(entry, ROUND_HR)
    controller = entry["controller"]
    state      = controller.state

    try:
        questions = controller.registry.hr_engine.get_questions(
            count=count
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Could not fetch HR questions: {str(exc)}"
        )

    # Persist questions so evaluate_answers() gets the same set
    state.hr_session_questions = questions

    return {
        "session_id":     session_id,
        "questions":      questions,
        "question_count": len(questions),
        "current_round":  ROUND_HR,
    }


# ─────────────────────────────────────────────────────────────────────────────
# POST /hr/submit
# ─────────────────────────────────────────────────────────────────────────────

@router.post("/hr/submit")
def submit_hr_answers(body: HRSubmitRequest):
    """
    Candidate submits answers to the HR questions.

    1. Validate that hr_session_questions were fetched
    2. evaluate_answers(questions, answers)  ← new HREngine method
    3. Compute final_hr_score
    4. Generate HR report
    5. Advance to FINAL round
    """

    entry      = require_session(body.session_id)
    require_round(entry, ROUND_HR)
    controller = entry["controller"]
    state      = controller.state

    questions = state.hr_session_questions

    if not questions:
        raise HTTPException(
            status_code=409,
            detail=(
                "No HR questions found for this session. "
                "Call GET /hr/questions/{session_id} first."
            )
        )

    if len(body.answers) != len(questions):
        raise HTTPException(
            status_code=422,
            detail=(
                f"Expected {len(questions)} answers, "
                f"got {len(body.answers)}."
            )
        )

    # ── 1. Evaluate answers ──────────────────────────
    try:
        results = controller.registry.hr_engine.evaluate_answers(
            questions=questions,
            answers=body.answers,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"HR evaluation failed: {str(exc)}"
        )

    state.hr_results = results

    scores = [
        r["evaluation"]["hr_score"]
        for r in results
    ]

    state.final_hr_score = round(
        sum(scores) / len(scores),
        2
    ) if scores else 0.0

    # ── 2. Generate HR report ────────────────────────
    try:
        controller.run_hr_report_phase()
    except Exception as exc:
        print(f"[WARN] HR report: {exc}")

    set_round(body.session_id, ROUND_FINAL)

    return {
        "session_id":     body.session_id,
        "hr_results":     results,
        "final_hr_score": state.final_hr_score,
        "hr_report":      state.hr_report,
        "current_round":  ROUND_FINAL,
        "next_action": (
            f"GET /api/v1/interview/final"
            f"/{body.session_id}"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# GET /final/{session_id}
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/final/{session_id}")
def get_final_result(session_id: str):
    """
    Aggregate all round scores, run Module8 evaluation,
    and return the complete interview verdict.

    Scoring weights (InterviewOrchestrator):
      ATS       20%
      Coding    40%
      Aptitude  20%
      Semantic  10%  ← real score, not hardcoded
      HR        10%
    """

    entry = require_session(session_id)

    if entry["current_round"] not in (ROUND_FINAL, ROUND_COMPLETE):
        raise HTTPException(
            status_code=409,
            detail=(
                f"Cannot access final results yet. "
                f"Current round: {entry['current_round']}"
            )
        )

    controller = entry["controller"]
    state      = controller.state

    print(f"\n[TRACE] GET /final/{session_id} started. final_coding_score: {state.final_coding_score}")

    # ── Run Module8 ──────────────────────────────────
    if entry["current_round"] != ROUND_COMPLETE:
        try:
            controller.run_module8_phase()
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Module8 evaluation failed: {str(exc)}"
            )
        set_round(session_id, ROUND_COMPLETE)

    ats_score      = (state.ats_result or {}).get("ats_score", 0)
    coding_score   = state.final_coding_score
    aptitude_score = state.final_aptitude_score
    semantic_score = state.final_semantic_score
    hr_score       = state.final_hr_score

    # Replicate the weighted formula from InterviewOrchestrator
    weighted_total = round(
        ats_score      * 0.20 +
        coding_score   * 0.40 +
        aptitude_score * 0.20 +
        semantic_score * 0.10 +
        hr_score       * 0.10,
        2
    )

    return {
        "session_id":   session_id,
        "candidate_id": state.candidate_id,

        "scores": {
            "ats_score":      ats_score,
            "coding_score":   coding_score,
            "aptitude_score": aptitude_score,
            "semantic_score": semantic_score,
            "hr_score":       hr_score,
        },

        "weighted_total": weighted_total,
        "level":          state.module8_result["level"],
        "next_round":     state.module8_result["next_round"],
        "module8_result": state.module8_result,

        "reports": {
            "coding_report":   state.coding_report,
            "aptitude_result": state.aptitude_result,
            "hr_report":       state.hr_report,
        },

        "generated_questions": state.generated_questions,
        "assessment_plan":     state.assessment_plan,
        "qgen_answers":        state.qgen_answers,

        "interview_complete": True,
    }


# ─────────────────────────────────────────────────────────────────────────────
# GET /status/{session_id}
# ─────────────────────────────────────────────────────────────────────────────

ROUND_ORDER = [
    ROUND_INIT,
    ROUND_ATS_DONE,
    ROUND_QGEN,
    ROUND_CODING,
    ROUND_APTITUDE,
    ROUND_HR,
    ROUND_FINAL,
    ROUND_COMPLETE,
]


@router.get("/status/{session_id}")
def get_session_status(session_id: str):
    """
    Return current round and completed rounds.
    Useful for frontend state recovery after page refresh.
    """

    entry = require_session(session_id)

    current = entry["current_round"]

    try:
        current_idx = ROUND_ORDER.index(current)
    except ValueError:
        current_idx = 0

    completed = ROUND_ORDER[:current_idx]

    return {
        "session_id":        session_id,
        "candidate_id":      entry["candidate_id"],
        "current_round":     current,
        "rounds_completed":  completed,
        "interview_complete": current == ROUND_COMPLETE,
        "created_at":        entry["created_at"].isoformat(),
    }
