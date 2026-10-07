from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.person import Person
from app.models.movie_credit import MovieCredit


def get_movie_analyst_context(
    db: Session,
    movie_id: int,
) -> dict | None:
    """
    Build structured movie context for the AI Movie Analyst.

    Data comes directly from CineScope's PostgreSQL database.
    """

    # ---------------------------------------------------------
    # Movie
    # ---------------------------------------------------------

    movie = db.scalar(
        select(Movie).where(
            Movie.id == movie_id
        )
    )

    if movie is None:
        return None


    # ---------------------------------------------------------
    # Genres
    # ---------------------------------------------------------

    genres = db.execute(
        select(Genre)
        .join(
            MovieGenre,
            MovieGenre.genre_id == Genre.id,
        )
        .where(
            MovieGenre.movie_id == movie_id
        )
    ).scalars().all()


    # ---------------------------------------------------------
    # Credits
    # ---------------------------------------------------------

    credits = db.execute(
        select(MovieCredit, Person)
        .join(
            Person,
            Person.id == MovieCredit.person_id,
        )
        .where(
            MovieCredit.movie_id == movie_id
        )
    ).all()


    actors = []
    directors = []

    for credit, person in credits:

        if credit.credit_type == "cast":
            actors.append({
                "name": person.name,
                "character": credit.character_name,
            })

        elif (
            credit.credit_type == "crew"
            and credit.job
            and credit.job.lower() == "director"
        ):
            directors.append({
                "name": person.name,
            })


    # ---------------------------------------------------------
    # Final structured context
    # ---------------------------------------------------------

    return {
        "movie": {
            "id": movie.id,
            "tmdb_id": movie.tmdb_id,
            "title": movie.title,
            "overview": movie.overview,
            "release_date": (
                movie.release_date.isoformat()
                if movie.release_date
                else None
            ),
            "rating": movie.rating,
            "vote_count": movie.vote_count,
            "popularity": movie.popularity,
        },

        "genres": [
            genre.name
            for genre in genres
        ],

        "actors": actors,

        "directors": directors,

        "has_embedding": movie.embedding is not None,
    }