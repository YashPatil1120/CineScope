from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.person import Person
from app.models.movie_credit import MovieCredit

from app.services.tmdb import TMDBService


def get_or_create_movie(
    db: Session,
    tmdb_id: int,
) -> Movie:

    # ============================================================
    # CHECK LOCAL DATABASE
    # ============================================================

    movie = db.scalar(
        select(Movie).where(
            Movie.tmdb_id == tmdb_id
        )
    )

    tmdb = TMDBService()

    # ============================================================
    # FETCH MOVIE DETAILS ONLY WHEN NEEDED
    # ============================================================
    #
    # movie_data is intentionally kept outside the creation block
    # so that the same TMDB response can also be used for genres.
    #
    # This prevents:
    #
    #     get_movie()
    #     get_movie() AGAIN
    #
    # for a newly imported movie.
    #
    # ============================================================

    movie_data = None

    if not movie:

        movie_data = tmdb.get_movie(
            tmdb_id
        )

        movie = Movie(
            tmdb_id=movie_data["id"],
            title=movie_data["title"],
            overview=movie_data.get("overview"),
            release_date=(
                date.fromisoformat(
                    movie_data["release_date"]
                )
                if movie_data.get("release_date")
                else None
            ),
            poster_path=movie_data.get(
                "poster_path"
            ),
            backdrop_path=movie_data.get(
                "backdrop_path"
            ),
            runtime=movie_data.get(
                "runtime"
            ),
            rating=movie_data.get(
                "vote_average"
            ),
            vote_count=movie_data.get(
                "vote_count"
            ),
            popularity=movie_data.get(
                "popularity"
            ),
            original_language=movie_data.get(
                "original_language"
            ),
        )

        db.add(movie)
        db.flush()

    # ============================================================
    # CHECK WHETHER GENRES ALREADY EXIST
    # ============================================================

    existing_genres = db.scalars(
        select(MovieGenre).where(
            MovieGenre.movie_id == movie.id
        )
    ).all()

    # ============================================================
    # IMPORT GENRES
    # ============================================================

    if not existing_genres:

        # --------------------------------------------------------
        # If the movie already existed locally, fetch its details
        # once so we can populate missing genres.
        #
        # If the movie was just created, movie_data already
        # contains the required genre information.
        # --------------------------------------------------------

        if movie_data is None:

            movie_data = tmdb.get_movie(
                tmdb_id
            )

        for genre_data in movie_data.get(
            "genres",
            [],
        ):

            genre = db.scalar(
                select(Genre).where(
                    Genre.tmdb_id
                    == genre_data["id"]
                )
            )

            if not genre:

                genre = Genre(
                    tmdb_id=genre_data["id"],
                    name=genre_data["name"],
                )

                db.add(genre)
                db.flush()

            existing_link = db.scalar(
                select(MovieGenre).where(
                    MovieGenre.movie_id == movie.id,
                    MovieGenre.genre_id == genre.id,
                )
            )

            if not existing_link:

                db.add(
                    MovieGenre(
                        movie_id=movie.id,
                        genre_id=genre.id,
                    )
                )

    # ============================================================
    # CHECK WHETHER CREDITS ALREADY EXIST
    # ============================================================

    existing_credits = db.scalars(
        select(MovieCredit).where(
            MovieCredit.movie_id == movie.id
        )
    ).all()

    # ============================================================
    # IMPORT CAST + DIRECTORS
    # ============================================================

    if not existing_credits:

        credits_data = tmdb.get_movie_credits(
            tmdb_id
        )

        # --------------------------------------------------------
        # CAST
        # --------------------------------------------------------

        for cast_member in credits_data.get(
            "cast",
            [],
        )[:10]:

            person = db.scalar(
                select(Person).where(
                    Person.tmdb_id
                    == cast_member["id"]
                )
            )

            if not person:

                person = Person(
                    tmdb_id=cast_member["id"],
                    name=cast_member["name"],
                    profile_path=cast_member.get(
                        "profile_path"
                    ),
                )

                db.add(person)
                db.flush()

            existing_credit = db.scalar(
                select(MovieCredit).where(
                    MovieCredit.movie_id == movie.id,
                    MovieCredit.person_id == person.id,
                    MovieCredit.credit_type == "cast",
                    MovieCredit.character_name
                    == cast_member.get("character"),
                )
            )

            if not existing_credit:

                db.add(
                    MovieCredit(
                        movie_id=movie.id,
                        person_id=person.id,
                        credit_type="cast",
                        character_name=cast_member.get(
                            "character"
                        ),
                        job=None,
                    )
                )

        # --------------------------------------------------------
        # DIRECTORS
        # --------------------------------------------------------

        for crew_member in credits_data.get(
            "crew",
            [],
        ):

            if (
                crew_member.get("job", "").lower()
                != "director"
            ):
                continue

            person = db.scalar(
                select(Person).where(
                    Person.tmdb_id
                    == crew_member["id"]
                )
            )

            if not person:

                person = Person(
                    tmdb_id=crew_member["id"],
                    name=crew_member["name"],
                    profile_path=crew_member.get(
                        "profile_path"
                    ),
                )

                db.add(person)
                db.flush()

            existing_credit = db.scalar(
                select(MovieCredit).where(
                    MovieCredit.movie_id == movie.id,
                    MovieCredit.person_id == person.id,
                    MovieCredit.credit_type == "crew",
                    MovieCredit.job == "Director",
                )
            )

            if not existing_credit:

                db.add(
                    MovieCredit(
                        movie_id=movie.id,
                        person_id=person.id,
                        credit_type="crew",
                        character_name=None,
                        job="Director",
                    )
                )

    # ============================================================
    # SAVE EVERYTHING
    # ============================================================

    db.commit()

    db.refresh(movie)

    return movie