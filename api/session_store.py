"""
api/session_store.py
────────────────────
In-memory session store for the interview API.

Each session entry holds:
  - controller    : live MasterController instance (preserves MCQEngine, CodingSession)
  - current_round : str — tracks which round the candidate is on
  - candidate_id  : str — candidate identifier
  - created_at    : datetime — for TTL cleanup

Round progression:
  INIT → ATS_DONE → QGEN → CODING → APTITUDE → HR → FINAL → COMPLETE
"""

from datetime import datetime, timedelta
from typing import Dict, Any


# ─────────────────────────────────────────────────────────────────────────────
# ROUND CONSTANTS
# Canonical round keys used as current_round values in the store.
# ─────────────────────────────────────────────────────────────────────────────

ROUND_INIT       = "INIT"
ROUND_ATS_DONE   = "ATS_DONE"
ROUND_QGEN       = "QGEN"
ROUND_CODING     = "CODING"
ROUND_APTITUDE   = "APTITUDE"
ROUND_HR         = "HR"
ROUND_FINAL      = "FINAL"
ROUND_COMPLETE   = "COMPLETE"


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STORE
# dict[session_id: str  →  session_entry: dict]
# ─────────────────────────────────────────────────────────────────────────────

SESSION_STORE: Dict[str, Dict[str, Any]] = {}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def create_session(
    session_id: str,
    controller,
    candidate_id: str,
    resume_filename: str = ""
) -> dict:
    """
    Create and register a new session entry.
    Returns the session entry dict.
    """
    entry = {
        "controller":       controller,
        "current_round":    ROUND_INIT,
        "candidate_id":     candidate_id,
        "resume_filename":  resume_filename,
        "created_at":       datetime.utcnow(),
    }

    SESSION_STORE[session_id] = entry

    return entry


def get_session(session_id: str) -> dict | None:
    """
    Retrieve a session by ID.
    Returns None if not found.
    """
    return SESSION_STORE.get(session_id)


def set_round(session_id: str, round_name: str) -> None:
    """Advance the current_round for a session."""
    if session_id in SESSION_STORE:
        SESSION_STORE[session_id]["current_round"] = round_name


def delete_session(session_id: str) -> None:
    """Remove a session from the store."""
    SESSION_STORE.pop(session_id, None)


def cleanup_expired_sessions(ttl_hours: int = 2) -> int:
    """
    Remove sessions older than `ttl_hours`.
    Returns the number of sessions evicted.
    Called by a background task or startup event.
    """
    cutoff = datetime.utcnow() - timedelta(hours=ttl_hours)

    expired = [
        sid
        for sid, entry in SESSION_STORE.items()
        if entry["created_at"] < cutoff
    ]

    for sid in expired:
        del SESSION_STORE[sid]

    return len(expired)
