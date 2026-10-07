from sqlalchemy import select

from app.db.session import get_session
from app.models.user import User
from app.services.recommendation import RecommendationService


def main():

    # ==========================================
    # GET DATABASE SESSION
    # ==========================================

    db = next(get_session())

    try:

        # ======================================
        # GET FIRST USER
        # ======================================

        user = db.scalar(
            select(User)
            .order_by(User.id)
        )

        if not user:

            print(
                "No users found in the database."
            )

            return

        print()
        print("=" * 60)
        print("CINESCOPE RECOMMENDATION ENGINE TEST")
        print("=" * 60)

        print()
        print(
            f"User: {user.username}"
        )

        print(
            f"User ID: {user.id}"
        )

        # ======================================
        # RUN RECOMMENDATION ENGINE
        # ======================================

        service = RecommendationService()

        recommendations = (
            service.get_recommendations(
                db=db,
                user_id=user.id,
                limit=10,
            )
        )

        print()
        print("-" * 60)
        print("RECOMMENDATIONS")
        print("-" * 60)

        if not recommendations:

            print()
            print(
                "No recommendations available."
            )

            print(
                "The user may not have enough "
                "watched movie history yet."
            )

            return

        # ======================================
        # DISPLAY RESULTS
        # ======================================

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            movie = recommendation["movie"]

            score = recommendation["score"]
            content_score = recommendation["content_score"]
            quality_score = recommendation["quality_score"]

            explanation = recommendation["explanation"]

            matched_genres = explanation["genres"]
            matched_actors = explanation["actors"]
            matched_directors = explanation["directors"]

            print()
            print(
                f"{index}. {movie.title}"
            )

            print(
                f"   Movie ID: {movie.id}"
            )

            print(
                f"   TMDB ID: {movie.tmdb_id}"
            )

            print(
                f"   TMDB Rating: "
                f"{movie.rating}"
            )

            print(
                f"   Recommendation Score: "
                f"{score}"
            )

            print(
                f"   Content Score: "
                f"{content_score}"
            )

            print(
                f"   Quality Score: "
                f"{quality_score}"
            )

            # ==================================
            # RECOMMENDATION EXPLANATION
            # ==================================

            print()
            print("   Why this movie?")

            if matched_genres:

                print(
                    "   Genres: "
                    + ", ".join(matched_genres)
                )

            else:

                print(
                    "   Genres: None"
                )

            if matched_actors:

                print(
                    "   Actors: "
                    + ", ".join(matched_actors)
                )

            else:

                print(
                    "   Actors: None"
                )

            if matched_directors:

                print(
                    "   Directors: "
                    + ", ".join(matched_directors)
                )

            else:

                print(
                    "   Directors: None"
                )

        print()
        print("=" * 60)
        print("TEST COMPLETED")
        print("=" * 60)
        print()

    finally:

        db.close()


if __name__ == "__main__":
    main()