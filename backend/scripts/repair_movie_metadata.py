from sqlalchemy import select

from app.db.session import get_session
from app.models.movie import Movie
from app.models.movie_genre import MovieGenre
from app.models.movie_credit import MovieCredit
from app.services.movie_importer import get_or_create_movie


TMDB_ID = 157336


def main():

    db = next(get_session())

    try:

        print()
        print("=" * 60)
        print("CINESCOPE MOVIE METADATA REPAIR")
        print("=" * 60)

        # ======================================================
        # RUN IMPORTER
        # ======================================================

        movie = get_or_create_movie(
            db=db,
            tmdb_id=TMDB_ID,
        )

        print()
        print(f"Movie: {movie.title}")
        print(f"Database ID: {movie.id}")
        print(f"TMDB ID: {movie.tmdb_id}")

        # ======================================================
        # CHECK GENRES
        # ======================================================

        genres = db.scalars(
            select(MovieGenre).where(
                MovieGenre.movie_id == movie.id
            )
        ).all()

        print()
        print(
            f"Genres imported: {len(genres)}"
        )

        # ======================================================
        # CHECK CREDITS
        # ======================================================

        credits = db.scalars(
            select(MovieCredit).where(
                MovieCredit.movie_id == movie.id
            )
        ).all()

        cast_count = sum(
            1
            for credit in credits
            if credit.credit_type == "cast"
        )

        director_count = sum(
            1
            for credit in credits
            if (
                credit.credit_type == "crew"
                and credit.job
                and credit.job.lower()
                == "director"
            )
        )

        print(
            f"Cast imported: {cast_count}"
        )

        print(
            f"Directors imported: {director_count}"
        )

        print()
        print("=" * 60)
        print("METADATA REPAIR COMPLETED")
        print("=" * 60)
        print()

    finally:

        db.close()


if __name__ == "__main__":
    main()