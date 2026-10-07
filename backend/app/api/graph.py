from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.graph import MovieGraphResponse
from app.services.graph import get_movie_graph


router = APIRouter(
    prefix="/api/graph",
    tags=["Knowledge Graph"],
)


@router.get(
    "/movie/{movie_id}",
    response_model=MovieGraphResponse,
)
def movie_graph(
    movie_id: int,
    db: Session = Depends(get_db),
):
    graph = get_movie_graph(
        db=db,
        movie_id=movie_id,
    )

    if graph is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found",
        )

    return graph