import time
import sys

_STARTUP_T0 = time.perf_counter()
print(f"[main] Python {sys.version} – import chain starting …", flush=True)

from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

print(f"[main] FastAPI imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.routes.coding import (
    router as coding_router
)
print(f"[main] coding router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.routes.candidate import (
    router as candidate_router
)
print(f"[main] candidate router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.routes.evaluate import (
    router as evaluate_router
)
print(f"[main] evaluate router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.routes.analytics import (
    router as analytics_router
)
print(f"[main] analytics router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.routes.recruiter import (
    router as recruiter_router
)
print(f"[main] recruiter router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.routes.executive import (
    router as executive_router
)
print(f"[main] executive router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

# ── Phase 8C: Session-based interview router ────────
from api.routes.interview import (
    router as interview_router
)
print(f"[main] interview router imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)

from api.session_store import (
    cleanup_expired_sessions
)
print(f"[main] session_store imported ({time.perf_counter()-_STARTUP_T0:.2f}s)", flush=True)


app = FastAPI(
    title="AI Mock Interviewer API",
    description=(
        "Multi-round AI interview system: "
        "ATS → QGEN → Coding → Aptitude → HR → Module8"
    ),
    version="8C",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ── CORS ────────────────────────────────────────────

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ── STARTUP / SHUTDOWN ──────────────────────────────

@app.on_event("startup")
async def on_startup():
    """Evict any stale sessions from a prior run."""
    t0 = time.perf_counter()
    print("[startup] on_startup() called …", flush=True)
    evicted = cleanup_expired_sessions(ttl_hours=2)
    print(f"[startup] Cleaned {evicted} expired sessions.", flush=True)
    print(f"[startup] Done in {time.perf_counter()-t0:.2f}s – app ready.", flush=True)


# ── REGISTER ROUTERS ────────────────────────────────

# Existing routers
app.include_router(evaluate_router)
app.include_router(analytics_router)
app.include_router(recruiter_router)
app.include_router(executive_router)
app.include_router(candidate_router)
app.include_router(coding_router)

# Phase 8C — session interview flow
app.include_router(interview_router)


# ── ROOT ─────────────────────────────────────────────

@app.get("/")
def home():
    return {
        "message": "AI Interview Copilot API Running",
        "version": "8C — Session Flow Active",
        "docs":    "/docs",
        "interview_flow": {
            "start":             "POST  /api/v1/interview/start",
            "qgen_submit":       "POST  /api/v1/interview/qgen/submit",
            "coding_problem":    "GET   /api/v1/interview/coding/problem/{session_id}",
            "coding_submit":     "POST  /api/v1/interview/coding/submit",
            "aptitude_questions":"GET   /api/v1/interview/aptitude/questions/{session_id}",
            "aptitude_submit":   "POST  /api/v1/interview/aptitude/submit",
            "hr_questions":      "GET   /api/v1/interview/hr/questions/{session_id}",
            "hr_submit":         "POST  /api/v1/interview/hr/submit",
            "final":             "GET   /api/v1/interview/final/{session_id}",
            "status":            "GET   /api/v1/interview/status/{session_id}",
        }
    }


# ── DASHBOARD (legacy) ────────────────────────────────

@app.get("/dashboard-data")
def get_dashboard_data(session_id: str = None):
    from api.session_store import SESSION_STORE, ROUND_COMPLETE, ROUND_FINAL, get_session
    
    entry = None
    if session_id:
        entry = get_session(session_id)
        
    if not entry:
        # Load the most recent completed interview instead
        completed_sessions = [
            (sid, e) for sid, e in SESSION_STORE.items() 
            if e["current_round"] in (ROUND_COMPLETE, ROUND_FINAL)
        ]
        if completed_sessions:
            completed_sessions.sort(key=lambda x: x[1]["created_at"], reverse=True)
            entry = completed_sessions[0][1]
            
    if not entry:
        return {"error": "No active session or data available."}
        
    state = entry["controller"].state
    
    # Extract scores
    ats_score = state.final_ats_score or 0.0
    coding_score = state.final_coding_score or 0
    aptitude_score = state.final_aptitude_score or 0
    semantic_score = state.final_semantic_score or 0
    hr_score = state.final_hr_score or 0
    
    # Calculate confidence based on weighted total (rough mapping)
    weighted_total = (
        ats_score * 0.20 +
        coding_score * 0.40 +
        aptitude_score * 0.20 +
        semantic_score * 0.10 +
        hr_score * 0.10
    )
    
    if weighted_total >= 80:
        confidence = "High"
    elif weighted_total >= 60:
        confidence = "Medium"
    else:
        confidence = "Low"
        
    # Get HR strengths and weaknesses
    hr_report = state.hr_report or {}
    strengths = hr_report.get("strengths", [])
    weaknesses = hr_report.get("improvements", [])
    
    # Module 8 Decision mapping
    level = state.module8_result.get("level", "AVERAGE") if state.module8_result else "AVERAGE"
    if level == "EXCELLENT":
        verdict = "Hire"
        role_fit = "Senior / Advanced Role"
        salary_band = "15-25 LPA"
    elif level == "GOOD":
        verdict = "Strong Consideration"
        role_fit = "Mid-Level Role"
        salary_band = "8-15 LPA"
    elif level == "AVERAGE":
        verdict = "Consider"
        role_fit = "Junior Role"
        salary_band = "4-8 LPA"
    else:
        verdict = "Needs Improvement"
        role_fit = "Entry Level"
        salary_band = "3-5 LPA"
        
    ai_rec = state.module8_result.get("ai_recommendation", "") if state.module8_result else "No recommendation yet."

    return {
        "ats_score": ats_score,
        "coding_score": coding_score,
        "semantic_score": semantic_score,
        "aptitude_score": aptitude_score,
        "hr_score": hr_score,
        "recruiter_confidence": confidence,
        "confidence_percent": round(weighted_total),
        "executive_summary": ai_rec,
        "feedback": {
            "strengths": strengths,
            "weaknesses": weaknesses
        },
        "recruiter_report": {
            "hiring_confidence": confidence,
            "role_fit": role_fit,
            "salary_band": salary_band,
            "final_verdict": verdict
        },
        "analytics_report": {
            "average_score": round(weighted_total)
        },
        "performance": [
            {"round": "ATS", "score": ats_score},
            {"round": "Coding", "score": coding_score},
            {"round": "Aptitude", "score": aptitude_score},
            {"round": "Technical", "score": semantic_score},
            {"round": "HR", "score": hr_score}
        ]
    }