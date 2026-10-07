from pydantic import BaseModel, Field


class MovieInteractionCreate(BaseModel):
    watched: bool = False
    rating: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )


class MovieInteractionUpdate(BaseModel):
    watched: bool | None = None
    rating: int | None = Field(
        default=None,
        ge=1,
        le=10,
    )


class MovieInteractionResponse(BaseModel):
    id: int
    movie_id: int
    tmdb_id: int
    title: str
    poster_path: str | None
    watched: bool
    rating: int | None

    model_config = {
        "from_attributes": True
    }