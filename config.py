import os
from dotenv import load_dotenv

# Load from .env if present
load_dotenv()

# Absolute path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Database Configurations
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin")
DB_NAME = os.getenv("DB_NAME", "ai_interviewer")

# Primary SQLAlchemy URL (defaults to SQLite if not provided)
# Note: Railway provides DATABASE_URL for Postgres/MySQL automatically
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(PROJECT_ROOT, 'ai_interview.db')}")

# External Services
JUDGE0_URL = os.getenv("JUDGE0_URL", "http://localhost:2358")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Server / Frontend Configurations
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

# Paths
UPLOADS_DIR = os.getenv("UPLOADS_DIR", os.path.join(PROJECT_ROOT, "uploads"))
