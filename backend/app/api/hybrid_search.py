from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.semantic_search import SemanticSearchResult
from app.services.hybrid_search import HybridSearchService


router = APIRouter(
    prefix="/api/movies",
    tags=["Hybrid Search"],
)


@router.get(
    "/hybrid-search",
    response_model=list[SemanticSearchResult],
)
def hybrid_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    db: Session = Depends(get_session),
):

    service = HybridSearchService()

    movies = service.search(
        db=db,
        query=q,
        limit=limit,
    )

    return movies