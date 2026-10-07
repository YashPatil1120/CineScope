from pydantic import BaseModel, Field


class AnalystRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=1000,
    )

    movie_id: int | None = Field(
        default=None,
        gt=0,
    )


class AnalystResponse(BaseModel):
    answer: str
    intent: str
    movies: list[dict] = []
    semantic_matches: list[dict] = []
    context_used: list[str] = []