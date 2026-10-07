from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_session
from app.models.movie import Movie
from app.models.movie_interaction import MovieInteraction
from app.models.user import User
from app.schemas.movie_interaction import (
    MovieInteractionCreate,
    MovieInteractionUpdate,
    MovieInteractionResponse,
)
from app.services.movie_importer import get_or_create_movie


router = APIRouter(
    prefix="/api/interactions",
    tags=["Movie Interactions"],
)


@router.post(
    "/tmdb/{tmdb_id}",
    response_model=MovieInteractionResponse,
    status_code=201,
)
def create_interaction(
    tmdb_id: int,
    interaction_data: MovieInteractionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    movie = get_or_create_movie(
        db=db,
        tmdb_id=tmdb_id,
    )

    existing_interaction = db.scalar(
        select(MovieInteraction).where(
            MovieInteraction.user_id == current_user.id,
            MovieInteraction.movie_id == movie.id,
        )
    )

    if existing_interaction:
        raise HTTPException(
            status_code=409,
            detail="Interaction already exists for this movie.",
        )

    interaction = MovieInteraction(
        user_id=current_user.id,
        movie_id=movie.id,
        watched=interaction_data.watched,
        rating=interaction_data.rating,
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return {
        "id": interaction.id,
        "movie_id": movie.id,
        "tmdb_id": movie.tmdb_id,
        "title": movie.title,
        "poster_path": movie.poster_path,
        "watched": interaction.watched,
        "rating": interaction.rating,
    }


@router.get(
    "",
    response_model=list[MovieInteractionResponse],
)
def get_interactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    interactions = db.scalars(
        select(MovieInteraction)
        .where(
            MovieInteraction.user_id == current_user.id
        )
        .order_by(
            MovieInteraction.updated_at.desc()
        )
    ).all()

    results = []

    for interaction in interactions:
        movie = db.get(
            Movie,
            interaction.movie_id,
        )

        if movie:
            results.append(
                {
                    "id": interaction.id,
                    "movie_id": movie.id,
                    "tmdb_id": movie.tmdb_id,
                    "title": movie.title,
                    "poster_path": movie.poster_path,
                    "watched": interaction.watched,
                    "rating": interaction.rating,
                }
            )

    return results


@router.patch(
    "/{movie_id}",
    response_model=MovieInteractionResponse,
)
def update_interaction(
    movie_id: int,
    interaction_data: MovieInteractionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    interaction = db.scalar(
        select(MovieInteraction).where(
            MovieInteraction.user_id == current_user.id,
            MovieInteraction.movie_id == movie_id,
        )
    )

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Movie interaction not found.",
        )

    if interaction_data.watched is not None:
        interaction.watched = (
            interaction_data.watched
        )

    if interaction_data.rating is not None:
        interaction.rating = (
            interaction_data.rating
        )

    db.commit()
    db.refresh(interaction)

    movie = db.get(
        Movie,
        interaction.movie_id,
    )

    return {
        "id": interaction.id,
        "movie_id": movie.id,
        "tmdb_id": movie.tmdb_id,
        "title": movie.title,
        "poster_path": movie.poster_path,
        "watched": interaction.watched,
        "rating": interaction.rating,
    }


@router.delete(
    "/{movie_id}",
)
def delete_interaction(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    interaction = db.scalar(
        select(MovieInteraction).where(
            MovieInteraction.user_id == current_user.id,
            MovieInteraction.movie_id == movie_id,
        )
    )

    if not interaction:
        raise HTTPException(
            status_code=404,
            detail="Movie interaction not found.",
        )

    db.delete(interaction)
    db.commit()

    return {
        "message": "Movie interaction removed.",
        "movie_id": movie_id,
    }