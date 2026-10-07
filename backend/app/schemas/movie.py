from datetime import date

from pydantic import BaseModel, ConfigDict


class GenreResponse(BaseModel):
    id: int
    tmdb_id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class PersonResponse(BaseModel):
    id: int
    tmdb_id: int
    name: str
    profile_path: str | None

    model_config = ConfigDict(
        from_attributes=True
    )


class CastResponse(BaseModel):
    person: PersonResponse
    character_name: str | None


class DirectorResponse(BaseModel):
    person: PersonResponse


class MovieResponse(BaseModel):
    id: int
    tmdb_id: int
    title: str
    overview: str | None
    release_date: date | None
    poster_path: str | None
    backdrop_path: str | None
    runtime: int | None
    rating: float | None
    vote_count: int | None
    popularity: float | None
    original_language: str | None

    model_config = ConfigDict(
        from_attributes=True
    )


class MovieDetailResponse(MovieResponse):
    genres: list[GenreResponse]
    cast: list[CastResponse]
    directors: list[DirectorResponse]