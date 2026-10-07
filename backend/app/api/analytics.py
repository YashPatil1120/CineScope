from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.services.analytics import (
    get_user_overview,
    get_rating_distribution,
    get_favorite_genres,
    get_favorite_actors,
    get_favorite_directors,
    get_recently_watched,
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get("/overview")
def analytics_overview(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_user_overview(
        db=db,
        user_id=current_user.id,
    )

# ============================================================
# RATING DISTRIBUTION
# ============================================================

@router.get("/ratings")
def analytics_ratings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_rating_distribution(
        db=db,
        user_id=current_user.id,
    )

# ============================================================
# FAVORITE GENRES
# ============================================================

@router.get("/genres")
def analytics_genres(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_favorite_genres(
        db=db,
        user_id=current_user.id,
    )

# ============================================================
# FAVORITE ACTORS
# ============================================================

@router.get("/actors")
def analytics_actors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_favorite_actors(
        db=db,
        user_id=current_user.id,
    )

# ============================================================
# FAVORITE DIRECTORS
# ============================================================

@router.get("/directors")
def analytics_directors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_favorite_directors(
        db=db,
        user_id=current_user.id,
    )

# ============================================================
# RECENTLY WATCHED
# ============================================================

@router.get("/recent")
def analytics_recently_watched(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return get_recently_watched(
        db=db,
        user_id=current_user.id,
        limit=10,
    )