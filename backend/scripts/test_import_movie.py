import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

from sqlalchemy import func, select

from app.db.session import get_session

from app.models.movie_genre import MovieGenre
from app.models.movie_credit import MovieCredit

from app.services.movie_importer import (
    get_or_create_movie,
)


TMDB_ID = 1377237


def main():

    print("=" * 60)
    print("CineScope - Single Movie Import Test")
    print("=" * 60)

    db = next(
        get_session()
    )

    try:

        print(
            f"\nImporting TMDB movie: {TMDB_ID}"
        )

        movie = get_or_create_movie(
            db=db,
            tmdb_id=TMDB_ID,
        )

        print("\nIMPORT SUCCESSFUL")
        print("-" * 60)

        print(
            f"Database ID : {movie.id}"
        )

        print(
            f"TMDB ID     : {movie.tmdb_id}"
        )

        print(
            f"Title       : {movie.title}"
        )

        print(
            f"Release     : {movie.release_date}"
        )

        print(
            f"Rating      : {movie.rating}"
        )

        print(
            f"Vote Count  : {movie.vote_count}"
        )

        # ========================================================
        # VERIFY GENRES
        # ========================================================

        genre_count = db.scalar(
            select(
                func.count()
            )
            .select_from(MovieGenre)
            .where(
                MovieGenre.movie_id == movie.id
            )
        )

        print(
            f"Genres      : {genre_count}"
        )

        # ========================================================
        # VERIFY CREDITS
        # ========================================================

        credit_count = db.scalar(
            select(
                func.count()
            )
            .select_from(MovieCredit)
            .where(
                MovieCredit.movie_id == movie.id
            )
        )

        print(
            f"Credits     : {credit_count}"
        )

        print("\n" + "=" * 60)
        print("Single movie import test completed.")
        print("=" * 60)

    except Exception as error:

        db.rollback()

        print(
            "\nIMPORT FAILED:"
        )

        print(error)

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()