import os

from dotenv import load_dotenv


load_dotenv()


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")


# ============================================================
# TMDB
# ============================================================

TMDB_API_TOKEN = os.getenv("TMDB_API_TOKEN")


# ============================================================
# JWT
# ============================================================

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

JWT_ALGORITHM = "HS256"

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ============================================================
# REQUIRED ENVIRONMENT VARIABLES
# ============================================================

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured"
    )


if not TMDB_API_TOKEN:
    raise ValueError(
        "TMDB_API_TOKEN is not configured"
    )


if not JWT_SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY is not configured"
    )