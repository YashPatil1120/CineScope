import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)
from datetime import date, datetime

from sqlalchemy import select

from app.db.session import get_session
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.person import Person
from app.models.movie_genre import MovieGenre
from app.models.movie_credit import MovieCredit
from app.services.tmdb import TMDBService


def parse_date(value):
    if not value:
        return None

    return date.fromisoformat(value)


def get_or_create_genre(db, genre_data):
    genre = db.scalar(
        select(Genre).where(
            Genre.tmdb_id == genre_data["id"]
        )
    )

    if genre:
        return genre

    genre = Genre(
        tmdb_id=genre_data["id"],
        name=genre_data["name"],
    )

    db.add(genre)
    db.flush()

    return genre


def get_or_create_person(db, person_data):
    person = db.scalar(
        select(Person).where(
            Person.tmdb_id == person_data["id"]
        )
    )

    if person:
        return person

    person = Person(
        tmdb_id=person_data["id"],
        name=person_data["name"],
        profile_path=person_data.get("profile_path"),
    )

    db.add(person)
    db.flush()

    return person


def add_movie_genre(db, movie, genre):
    existing = db.scalar(
        select(MovieGenre).where(
            MovieGenre.movie_id == movie.id,
            MovieGenre.genre_id == genre.id,
        )
    )

    if not existing:
        db.add(
            MovieGenre(
                movie_id=movie.id,
                genre_id=genre.id,
            )
        )


def add_movie_credit(
    db,
    movie,
    person,
    credit_type,
    character_name=None,
    job=None,
):
    existing = db.scalar(
        select(MovieCredit).where(
            MovieCredit.movie_id == movie.id,
            MovieCredit.person_id == person.id,
            MovieCredit.credit_type == credit_type,
            MovieCredit.character_name == character_name,
            MovieCredit.job == job,
        )
    )

    if not existing:
        db.add(
            MovieCredit(
                movie_id=movie.id,
                person_id=person.id,
                credit_type=credit_type,
                character_name=character_name,
                job=job,
            )
        )

def import_movie(db, tmdb, tmdb_id):
    details = tmdb.get_movie(tmdb_id)
    credits = tmdb.get_movie_credits(tmdb_id)

    movie = db.scalar(
        select(Movie).where(
            Movie.tmdb_id == tmdb_id
        )
    )

    if movie:
      print(f"Updating: {details['title']}")

      movie.title = details["title"]
      movie.overview = details.get("overview")
      movie.release_date = parse_date(
        details.get("release_date")
        )
      movie.poster_path = details.get("poster_path")
      movie.backdrop_path = details.get("backdrop_path")
      movie.runtime = details.get("runtime")
      movie.rating = details.get("vote_average")
      movie.vote_count = details.get("vote_count")
      movie.popularity = details.get("popularity")
      movie.original_language = details.get(
        "original_language"
        )
      movie.updated_at = datetime.utcnow()

    else:
        print(f"Adding: {details['title']}")

        movie = Movie(
        tmdb_id=tmdb_id,
        title=details["title"],
        overview=details.get("overview"),
        release_date=parse_date(
            details.get("release_date")
        ),
        poster_path=details.get("poster_path"),
        backdrop_path=details.get("backdrop_path"),
        runtime=details.get("runtime"),
        rating=details.get("vote_average"),
        vote_count=details.get("vote_count"),
        popularity=details.get("popularity"),
        original_language=details.get(
            "original_language"
        ),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.add(movie)
    db.flush()

    # Genres
    for genre_data in details.get("genres", []):
        genre = get_or_create_genre(
            db,
            genre_data,
        )

        add_movie_genre(
            db,
            movie,
            genre,
        )

    # Top 10 cast members
    for person_data in credits.get("cast", [])[:10]:
        person = get_or_create_person(
            db,
            person_data,
        )

        add_movie_credit(
            db,
            movie,
            person,
            credit_type="cast",
            character_name=person_data.get(
                "character"
            ),
        )

    # Directors
    for person_data in credits.get("crew", []):
        if person_data.get("job") != "Director":
            continue

        person = get_or_create_person(
            db,
            person_data,
        )

        add_movie_credit(
            db,
            movie,
            person,
            credit_type="crew",
            job="Director",
        )

    db.commit()


def main():
    tmdb = TMDBService()
    db = get_session()

    try:
        print("Fetching popular movies from TMDB...")

        popular = tmdb.get_popular_movies(page=1)

        movies = popular["results"][:20]

        print(
            f"Found {len(movies)} movies to import.\n"
        )

        for index, movie_data in enumerate(
            movies,
            start=1,
        ):
            print(
                f"[{index}/{len(movies)}] "
                f"Processing {movie_data['title']}"
            )

            try:
                import_movie(
                    db,
                    tmdb,
                    movie_data["id"],
                )

            except Exception as error:
                db.rollback()

                print(
                    f"  ERROR: {error}"
                )

        print("\nImport completed.")

    finally:
        db.close()
        tmdb.close()


if __name__ == "__main__":
    main()