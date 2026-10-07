from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.semantic_search import SemanticSearchResult
from app.services.semantic_search import SemanticSearchService


router = APIRouter(
    prefix="/api/movies",
    tags=["Semantic Search"],
)


@router.get(
    "/semantic-search",
    response_model=list[SemanticSearchResult],
)
def semantic_search(
    q: str = Query(
        ...,
        min_length=2,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    db: Session = Depends(get_session),
):

    service = SemanticSearchService()

    movies = service.search(
        db=db,
        query=q,
        limit=limit,
    )

    return movies