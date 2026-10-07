from datetime import date

from pydantic import BaseModel


class MovieSearchResult(BaseModel):
    tmdb_id: int
    title: str
    overview: str | None
    release_date: date | None
    poster_path: str | None
    backdrop_path: str | None
    rating: float
    vote_count: int


class MovieSearchResponse(BaseModel):
    page: int
    total_pages: int
    total_results: int
    results: list[MovieSearchResult]