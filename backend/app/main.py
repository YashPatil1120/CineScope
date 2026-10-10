import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.api.auth import router as auth_router
from app.db.database import Base, engine
from app.models.movie import Movie
from app.api.movies import router as movies_router
from app.api.watchlist import router as watchlist_router
from app.api.movie_interactions import router as movie_interactions_router
from app.api.recommendations import router as recommendations_router
from app.api.semantic_search import router as semantic_search_router
from app.api.hybrid_search import router as hybrid_search_router
from app.api.analytics import router as analytics_router
from app.api.graph import router as graph_router
from app.api.analyst import router as analyst_router

app = FastAPI(
    title="CineScope API",
    description="Intelligent Movie Discovery & Recommendation Platform",
    version="1.0.0",
)



frontend_url = os.getenv("FRONTEND_URL", "").rstrip("/")

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(hybrid_search_router)
app.include_router(semantic_search_router)
app.include_router(graph_router)
app.include_router(analyst_router)
app.include_router(movies_router)
app.include_router(auth_router)
app.include_router(watchlist_router)
app.include_router(movie_interactions_router)
app.include_router(recommendations_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CineScope API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/db")
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as error:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(error),
        }