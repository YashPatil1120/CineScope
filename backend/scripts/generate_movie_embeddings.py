import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

from sqlalchemy import select

from app.db.session import get_session
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.person import Person
from app.models.movie_credit import MovieCredit
from app.services.embedding import embedding_service


def build_movie_text(
    db,
    movie: Movie,
) -> str:

    parts = [
        f"Title: {movie.title}",
    ]

    if movie.overview:
        parts.append(
            f"Overview: {movie.overview}"
        )

    # ==========================================================
    # GENRES
    # ==========================================================

    genre_links = db.scalars(
        select(MovieGenre)
        .where(
            MovieGenre.movie_id == movie.id
        )
    ).all()

    genres = []

    for genre_link in genre_links:

        genre = db.get(
            Genre,
            genre_link.genre_id
        )

        if genre:
            genres.append(
                genre.name
            )

    if genres:
        parts.append(
            f"Genres: {', '.join(genres)}"
        )

    # ==========================================================
    # CAST + DIRECTORS
    # ==========================================================

    credits = db.scalars(
        select(MovieCredit)
        .where(
            MovieCredit.movie_id == movie.id
        )
    ).all()

    actors = []
    directors = []

    for credit in credits:

        person = db.get(
            Person,
            credit.person_id
        )

        if not person:
            continue

        if credit.credit_type == "cast":

            actors.append(
                person.name
            )

        elif (
            credit.credit_type == "crew"
            and credit.job
            and credit.job.lower() == "director"
        ):

            directors.append(
                person.name
            )

    if actors:
        parts.append(
            f"Cast: {', '.join(actors)}"
        )

    if directors:
        parts.append(
            f"Director: {', '.join(directors)}"
        )

    # ==========================================================
    # LANGUAGE
    # ==========================================================

    if movie.original_language:
        parts.append(
            f"Language: {movie.original_language}"
        )

    return "\n".join(parts)


def generate_embeddings():

    db = next(get_session())

    try:

        # ------------------------------------------------------
        # IMPORTANT:
        # Regenerate ALL embeddings because the source text
        # has changed.
        # ------------------------------------------------------

        movies = db.scalars(
            select(Movie)
        ).all()

        print(
            f"Movies requiring embeddings: "
            f"{len(movies)}"
        )

        if not movies:

            print(
                "No movies found."
            )

            return

        for index, movie in enumerate(
            movies,
            start=1,
        ):

            movie_text = build_movie_text(
                db,
                movie,
            )

            embedding = (
                embedding_service.generate_embedding(
                    movie_text
                )
            )

            movie.embedding = embedding

            print(
                f"[{index}/{len(movies)}] "
                f"Embedded: {movie.title}"
            )

        db.commit()

        print(
            f"\nSuccessfully generated embeddings "
            f"for {len(movies)} movies."
        )

    except Exception:

        db.rollback()

        raise

    finally:

        db.close()


if __name__ == "__main__":
    generate_embeddings()