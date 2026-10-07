import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

# ============================================================
# IMPORTS
# ============================================================

from sqlalchemy import select

from app.db.database import SessionLocal

from app.models.movie import Movie

from app.services.tmdb import TMDBService

from app.services.movie_importer import (
    get_or_create_movie,
)


# ============================================================
# CONFIGURATION
# ============================================================

START_PAGE = 11
END_PAGE = 50

SORT_BY = "popularity.desc"

VOTE_COUNT_GTE = 50


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("CineScope Catalog Expansion")
    print("=" * 60)

    print(f"Pages           : {START_PAGE} -> {END_PAGE}")
    print(f"Sort            : {SORT_BY}")
    print(f"Minimum votes   : {VOTE_COUNT_GTE}")
    print("=" * 60)

    db = SessionLocal()

    tmdb = TMDBService()

    imported = 0
    skipped = 0
    failed = 0
    discovered = 0

    try:

        # ====================================================
        # PROCESS DISCOVER PAGES
        # ====================================================

        for page in range(
            START_PAGE,
            END_PAGE + 1,
        ):

            print()
            print("=" * 60)
            print(
                f"PAGE {page}/{END_PAGE}"
            )
            print("=" * 60)

            try:

                response = tmdb.discover_movies(
                    page=page,
                    sort_by=SORT_BY,
                    vote_count_gte=VOTE_COUNT_GTE,
                )

            except Exception as error:

                print(
                    f"FAILED TO FETCH PAGE {page}:"
                )
                print(error)

                failed += 1

                continue

            movies = response.get(
                "results",
                [],
            )

            print(
                f"TMDB results: {len(movies)}"
            )

            discovered += len(movies)

            page_imported = 0
            page_skipped = 0
            page_failed = 0

            # ================================================
            # PROCESS MOVIES
            # ================================================

            for movie_data in movies:

                tmdb_id = movie_data.get(
                    "id"
                )

                title = movie_data.get(
                    "title",
                    "Unknown",
                )

                if not tmdb_id:
                    continue

                try:

                    # ----------------------------------------
                    # CHECK LOCAL DATABASE
                    # ----------------------------------------

                    existing_movie = db.scalar(
                        select(Movie).where(
                            Movie.tmdb_id == tmdb_id
                        )
                    )

                    # ----------------------------------------
                    # IMPORT / REPAIR MOVIE
                    # ----------------------------------------

                    movie = get_or_create_movie(
                        db=db,
                        tmdb_id=tmdb_id,
                    )

                    # ----------------------------------------
                    # COUNT RESULT
                    # ----------------------------------------

                    if existing_movie:

                        skipped += 1
                        page_skipped += 1

                        print(
                            f"  SKIP     | "
                            f"{tmdb_id} | "
                            f"{title}"
                        )

                    else:

                        imported += 1
                        page_imported += 1

                        print(
                            f"  IMPORT   | "
                            f"{tmdb_id} | "
                            f"{title}"
                        )

                except Exception as error:

                    db.rollback()

                    failed += 1
                    page_failed += 1

                    print(
                        f"  FAILED   | "
                        f"{tmdb_id} | "
                        f"{title}"
                    )

                    print(
                        f"           {error}"
                    )

            # ================================================
            # PAGE SUMMARY
            # ================================================

            print()
            print(
                f"Page complete:"
            )

            print(
                f"  Imported : {page_imported}"
            )

            print(
                f"  Skipped  : {page_skipped}"
            )

            print(
                f"  Failed   : {page_failed}"
            )

    finally:

        db.close()

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print("CATALOG EXPANSION COMPLETE")
    print("=" * 60)

    print(
        f"Pages processed : "
        f"{END_PAGE - START_PAGE + 1}"
    )

    print(
        f"Movies found    : {discovered}"
    )

    print(
        f"Imported        : {imported}"
    )

    print(
        f"Skipped         : {skipped}"
    )

    print(
        f"Failed          : {failed}"
    )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()