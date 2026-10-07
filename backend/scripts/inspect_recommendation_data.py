from sqlalchemy import select

from app.db.session import get_session
from app.models.movie import Movie
from app.models.movie_credit import MovieCredit
from app.models.movie_genre import MovieGenre
from app.models.genre import Genre
from app.models.person import Person
from app.models.movie_interaction import MovieInteraction
from app.models.user import User


def main():

    db = next(get_session())

    try:

        user = db.scalar(
            select(User)
            .order_by(User.id)
        )

        if not user:
            print("No users found.")
            return

        print()
        print("=" * 70)
        print("CINESCOPE RECOMMENDATION DATA INSPECTION")
        print("=" * 70)

        interactions = db.scalars(
            select(MovieInteraction)
            .where(
                MovieInteraction.user_id == user.id
            )
        ).all()

        print(f"\nUser: {user.username}")
        print(f"Interactions: {len(interactions)}")

        for interaction in interactions:

            movie = db.get(
                Movie,
                interaction.movie_id,
            )

            if not movie:
                continue

            print("\n" + "-" * 70)
            print(f"Movie: {movie.title}")
            print(f"Watched: {interaction.watched}")
            print(f"Rating: {interaction.rating}")

            # ==============================================
            # GENRES
            # ==============================================

            genre_links = db.scalars(
                select(MovieGenre)
                .where(
                    MovieGenre.movie_id == movie.id
                )
            ).all()

            genres = []

            for link in genre_links:

                genre = db.get(
                    Genre,
                    link.genre_id,
                )

                if genre:
                    genres.append(genre.name)

            print(
                "Genres:",
                ", ".join(genres)
                if genres
                else "None",
            )

            # ==============================================
            # CREDITS
            # ==============================================

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
                    credit.person_id,
                )

                if not person:
                    continue

                if credit.credit_type == "cast":

                    actors.append(person.name)

                elif (
                    credit.credit_type == "crew"
                    and credit.job
                    and credit.job.lower()
                    == "director"
                ):

                    directors.append(person.name)

            print(
                "Actors:",
                ", ".join(actors[:10])
                if actors
                else "None",
            )

            print(
                "Directors:",
                ", ".join(directors)
                if directors
                else "None",
            )

        print("\n" + "=" * 70)
        print("INSPECTION COMPLETED")
        print("=" * 70)
        print()

    finally:
        db.close()


if __name__ == "__main__":
    main()