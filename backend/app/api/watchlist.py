from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.services.movie_importer import get_or_create_movie
from app.core.dependencies import get_current_user
from app.db.session import get_session
from app.models.movie import Movie
from app.models.user import User
from app.models.watchlist import Watchlist


router = APIRouter(
    prefix="/api/watchlist",
    tags=["Watchlist"],
)


# ============================================================
# ADD MOVIE TO WATCHLIST
# ============================================================

@router.post(
    "/tmdb/{tmdb_id}",
    status_code=201,
)
def add_to_watchlist(
    tmdb_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    # ============================================================
    # GET OR IMPORT MOVIE
    # ============================================================

    movie = get_or_create_movie(
        db=db,
        tmdb_id=tmdb_id,
    )


    # ============================================================
    # CHECK DUPLICATE
    # ============================================================

    existing_item = db.scalar(
        select(Watchlist).where(
            Watchlist.user_id == current_user.id,
            Watchlist.movie_id == movie.id,
        )
    )

    if existing_item:
        raise HTTPException(
            status_code=409,
            detail="Movie is already in your watchlist.",
        )


    # ============================================================
    # ADD TO WATCHLIST
    # ============================================================

    watchlist_item = Watchlist(
        user_id=current_user.id,
        movie_id=movie.id,
    )

    db.add(watchlist_item)

    try:
        db.commit()
        db.refresh(watchlist_item)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Movie is already in your watchlist.",
        )


    return {
        "message": "Movie added to watchlist.",
        "watchlist_id": watchlist_item.id,
        "movie_id": movie.id,
        "tmdb_id": movie.tmdb_id,
    }

# ============================================================
# GET CURRENT USER'S WATCHLIST
# ============================================================

@router.get("")
def get_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    items = db.scalars(
        select(Watchlist)
        .where(
            Watchlist.user_id == current_user.id
        )
        .order_by(
            Watchlist.created_at.desc()
        )
    ).all()

    results = []

    for item in items:

        movie = db.get(
            Movie,
            item.movie_id,
        )

        if movie:
            results.append(
                {
                    "watchlist_id": item.id,
                    "movie_id": movie.id,
                    "tmdb_id": movie.tmdb_id,
                    "title": movie.title,
                    "poster_path": movie.poster_path,
                    "release_date": movie.release_date,
                    "rating": movie.rating,
                    "added_at": item.created_at,
                }
            )

    return results


# ============================================================
# REMOVE MOVIE FROM WATCHLIST
# ============================================================

@router.delete(
    "/{movie_id}",
)
def remove_from_watchlist(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    item = db.scalar(
        select(Watchlist).where(
            Watchlist.user_id == current_user.id,
            Watchlist.movie_id == movie_id,
        )
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Movie is not in your watchlist.",
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Movie removed from watchlist.",
        "movie_id": movie_id,
    }