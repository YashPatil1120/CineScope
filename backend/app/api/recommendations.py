from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.recommendation import RecommendationResponse
from app.services.recommendation import RecommendationService


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "",
    response_model=list[RecommendationResponse],
)
def get_recommendations(
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
    ),
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_session
    ),
):

    service = RecommendationService()

    recommendations = (
        service.get_recommendations(
            db=db,
            user_id=current_user.id,
            limit=limit,
        )
    )

    return recommendations