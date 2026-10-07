from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.services.tmdb import TMDBService
from app.db.session import get_session

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.person import Person
from app.models.movie_credit import MovieCredit

from app.schemas.movie import (
    MovieResponse,
    MovieDetailResponse,
    GenreResponse,
    PersonResponse,
    CastResponse,
    DirectorResponse,
)

from app.schemas.search import (
    MovieSearchResponse,
    MovieSearchResult,
)

from datetime import date


router = APIRouter(
    prefix="/api/movies",
    tags=["Movies"],
)


# ============================================================
# GET ALL MOVIES
# ============================================================

@router.get(
    "",
    response_model=list[MovieResponse],
)
def get_movies(
    db: Session = Depends(get_session),
):
    movies = db.scalars(
        select(Movie)
        .order_by(Movie.popularity.desc())
    ).all()

    return movies


# ============================================================
# SEARCH MOVIES
# ============================================================

@router.get(
    "/search",
    response_model=MovieSearchResponse,
)
def search_movies(
    q: str,
    page: int = 1,
):
    if not q.strip():
        return {
            "page": 1,
            "total_pages": 0,
            "total_results": 0,
            "results": [],
        }

    tmdb = TMDBService()

    data = tmdb.search_movies(
        query=q.strip(),
        page=page,
    )

    results = []

    for movie in data.get("results", []):
        release_date = movie.get("release_date")

        parsed_date = None

        if release_date:
            try:
                parsed_date = date.fromisoformat(release_date)
            except ValueError:
                parsed_date = None

        results.append(
            MovieSearchResult(
                tmdb_id=movie["id"],
                title=movie["title"],
                overview=movie.get("overview"),
                release_date=parsed_date,
                poster_path=movie.get("poster_path"),
                backdrop_path=movie.get("backdrop_path"),
                rating=movie.get("vote_average", 0),
                vote_count=movie.get("vote_count", 0),
            )
        )

    return MovieSearchResponse(
        page=data.get("page", 1),
        total_pages=data.get("total_pages", 0),
        total_results=data.get("total_results", 0),
        results=results,
    )


# ============================================================
# GET SIMILAR MOVIES FROM TMDB
# ============================================================

@router.get(
    "/tmdb/{tmdb_id}/similar",
    response_model=MovieSearchResponse,
)
def get_similar_movies(
    tmdb_id: int,
):
    tmdb = TMDBService()

    data = tmdb.get_similar_movies(
        tmdb_id=tmdb_id,
        page=1,
    )

    results = []

    for movie in data.get("results", []):
        release_date = movie.get("release_date")

        parsed_date = None

        if release_date:
            try:
                parsed_date = date.fromisoformat(release_date)
            except ValueError:
                parsed_date = None

        results.append(
            MovieSearchResult(
                tmdb_id=movie["id"],
                title=movie["title"],
                overview=movie.get("overview"),
                release_date=parsed_date,
                poster_path=movie.get("poster_path"),
                backdrop_path=movie.get("backdrop_path"),
                rating=movie.get("vote_average", 0),
                vote_count=movie.get("vote_count", 0),
            )
        )

    return MovieSearchResponse(
        page=data.get("page", 1),
        total_pages=data.get("total_pages", 0),
        total_results=data.get("total_results", 0),
        results=results,
    )


# ============================================================
# GET MOVIE DETAILS DIRECTLY FROM TMDB
# ============================================================

@router.get(
    "/tmdb/{tmdb_id}",
    response_model=MovieDetailResponse,
)
def get_tmdb_movie(
    tmdb_id: int,
):
    tmdb = TMDBService()

    details = tmdb.get_movie(tmdb_id)
    credits = tmdb.get_movie_credits(tmdb_id)

    # -------------------------
    # Genres
    # -------------------------

    genres = [
        GenreResponse(
            id=genre["id"],
            tmdb_id=genre["id"],
            name=genre["name"],
        )
        for genre in details.get("genres", [])
    ]

    # -------------------------
    # Cast
    # -------------------------

    cast = []

    for person in credits.get("cast", [])[:10]:
        cast.append(
            CastResponse(
                person=PersonResponse(
                    id=person["id"],
                    tmdb_id=person["id"],
                    name=person["name"],
                    profile_path=person.get("profile_path"),
                ),
                character_name=person.get("character"),
            )
        )

    # -------------------------
    # Directors
    # -------------------------

    directors = []

    for person in credits.get("crew", []):
        if person.get("job") == "Director":
            directors.append(
                DirectorResponse(
                    person=PersonResponse(
                        id=person["id"],
                        tmdb_id=person["id"],
                        name=person["name"],
                        profile_path=person.get("profile_path"),
                    )
                )
            )

    # -------------------------
    # Movie details
    # -------------------------

    return MovieDetailResponse(
        id=details["id"],
        tmdb_id=details["id"],
        title=details["title"],
        overview=details.get("overview"),
        release_date=(
            date.fromisoformat(details["release_date"])
            if details.get("release_date")
            else None
        ),
        poster_path=details.get("poster_path"),
        backdrop_path=details.get("backdrop_path"),
        runtime=details.get("runtime"),
        rating=details.get("vote_average"),
        vote_count=details.get("vote_count"),
        popularity=details.get("popularity"),
        original_language=details.get("original_language"),
        genres=genres,
        cast=cast,
        directors=directors,
    )


# ============================================================
# GET MOVIE FROM LOCAL DATABASE
# ============================================================

@router.get(
    "/{movie_id}",
    response_model=MovieDetailResponse,
)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_session),
):
    movie = db.get(Movie, movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found",
        )

    # -------------------------
    # Genres
    # -------------------------

    genre_rows = db.execute(
        select(Genre)
        .join(
            MovieGenre,
            MovieGenre.genre_id == Genre.id
        )
        .where(MovieGenre.movie_id == movie_id)
    ).scalars().all()

    genres = [
        GenreResponse.model_validate(genre)
        for genre in genre_rows
    ]

    # -------------------------
    # Cast
    # -------------------------

    cast_rows = db.execute(
        select(MovieCredit, Person)
        .join(
            Person,
            Person.id == MovieCredit.person_id
        )
        .where(
            MovieCredit.movie_id == movie_id,
            MovieCredit.credit_type == "cast",
        )
    ).all()

    cast = [
        CastResponse(
            person=PersonResponse.model_validate(person),
            character_name=credit.character_name,
        )
        for credit, person in cast_rows
    ]

    # -------------------------
    # Directors
    # -------------------------

    director_rows = db.execute(
        select(MovieCredit, Person)
        .join(
            Person,
            Person.id == MovieCredit.person_id
        )
        .where(
            MovieCredit.movie_id == movie_id,
            MovieCredit.credit_type == "crew",
            MovieCredit.job == "Director",
        )
    ).all()

    directors = [
        DirectorResponse(
            person=PersonResponse.model_validate(person)
        )
        for credit, person in director_rows
    ]

    # -------------------------
    # Final response
    # -------------------------

    return MovieDetailResponse(
        **MovieResponse.model_validate(movie).model_dump(),
        genres=genres,
        cast=cast,
        directors=directors,
    )