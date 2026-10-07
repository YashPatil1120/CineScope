from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.analyst import (
    AnalystRequest,
    AnalystResponse,
)
from app.services.analyst import analyze_question


router = APIRouter(
    prefix="/api/analyst",
    tags=["AI Movie Analyst"],
)


@router.post(
    "/ask",
    response_model=AnalystResponse,
)
def ask_analyst(
    request: AnalystRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return analyze_question(
        db=db,
        user_id=current_user.id,
        question=request.question,
        movie_id=request.movie_id,
    )