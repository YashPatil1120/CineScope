from pydantic import BaseModel

from app.schemas.movie import MovieResponse


class RecommendationExplanation(BaseModel):
    genres: list[str]
    actors: list[str]
    directors: list[str]


class RecommendationResponse(BaseModel):
    movie: MovieResponse
    score: float
    content_score: float
    quality_score: float
    explanation: RecommendationExplanation