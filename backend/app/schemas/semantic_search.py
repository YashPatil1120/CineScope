from datetime import date

from pydantic import BaseModel


class SemanticSearchResult(BaseModel):
    id: int
    tmdb_id: int
    title: str
    overview: str | None
    release_date: date | None
    poster_path: str | None
    rating: float | None
    vote_count: int | None