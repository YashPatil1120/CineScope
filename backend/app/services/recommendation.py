from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.person import Person
from app.models.movie_credit import MovieCredit
from app.models.movie_genre import MovieGenre
from app.models.movie_interaction import MovieInteraction


class RecommendationService:

    def get_recommendations(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
    ):

        # ======================================================
        # 1. GET USER INTERACTIONS
        # ======================================================

        interactions = db.scalars(
            select(MovieInteraction)
            .where(
                MovieInteraction.user_id == user_id
            )
        ).all()

        if not interactions:
            return []

        # ======================================================
        # 2. MOVIES ALREADY INTERACTED WITH
        # ======================================================

        interacted_movie_ids = {
            interaction.movie_id
            for interaction in interactions
        }

        # ======================================================
        # 3. BUILD USER PREFERENCE PROFILE
        # ======================================================

        preferred_genres = Counter()
        preferred_actors = Counter()
        preferred_directors = Counter()

        for interaction in interactions:

            # Only watched movies contribute to the
            # content preference profile.
            if not interaction.watched:
                continue

            movie = db.get(
                Movie,
                interaction.movie_id,
            )

            if not movie:
                continue

            # ==================================================
            # RATING WEIGHT
            # ==================================================

            if interaction.rating is None:

                rating_weight = 1.0

            elif interaction.rating >= 8:

                rating_weight = 2.0

            elif interaction.rating >= 6:

                rating_weight = 1.0

            elif interaction.rating == 5:

                rating_weight = 0.0

            else:

                # Low-rated movies should not strengthen
                # the user's preference for their content.
                rating_weight = -1.0

            # ==================================================
            # GENRES
            # ==================================================

            genre_links = db.scalars(
                select(MovieGenre)
                .where(
                    MovieGenre.movie_id == movie.id
                )
            ).all()

            for genre_link in genre_links:

                preferred_genres[
                    genre_link.genre_id
                ] += rating_weight

            # ==================================================
            # CAST + DIRECTORS
            # ==================================================

            credits = db.scalars(
                select(MovieCredit)
                .where(
                    MovieCredit.movie_id == movie.id
                )
            ).all()

            for credit in credits:

                # ACTOR
                if credit.credit_type == "cast":

                    preferred_actors[
                        credit.person_id
                    ] += rating_weight

                # DIRECTOR
                elif (
                    credit.credit_type == "crew"
                    and credit.job
                    and credit.job.lower()
                    == "director"
                ):

                    preferred_directors[
                        credit.person_id
                    ] += rating_weight

        # ======================================================
        # 4. GET CANDIDATE MOVIES
        # ======================================================

        candidate_movies = db.scalars(
            select(Movie)
            .where(
                Movie.id.not_in(
                    interacted_movie_ids
                )
            )
        ).all()

        # ======================================================
        # 5. SCORE CANDIDATE MOVIES
        # ======================================================

        recommendations = []

        for movie in candidate_movies:

            # --------------------------------------------------
            # EXPLANATION TRACKING
            # --------------------------------------------------

            matched_genres = []
            matched_actors = []
            matched_directors = []

            # --------------------------------------------------
            # GENRE MATCH
            # --------------------------------------------------

            genre_score = 0.0

            genre_links = db.scalars(
                select(MovieGenre)
                .where(
                    MovieGenre.movie_id == movie.id
                )
            ).all()

            for genre_link in genre_links:

                genre_contribution = preferred_genres.get(
                    genre_link.genre_id,
                    0,
                )

                genre_score += genre_contribution

                # Only positive preferences should be shown
                # as recommendation explanations.
                if genre_contribution > 0:

                    genre = db.get(
                        Genre,
                        genre_link.genre_id,
                    )

                    if genre:
                        matched_genres.append(
                            genre.name
                        )

            # --------------------------------------------------
            # ACTOR + DIRECTOR MATCH
            # --------------------------------------------------

            actor_score = 0.0
            director_score = 0.0

            credits = db.scalars(
                select(MovieCredit)
                .where(
                    MovieCredit.movie_id == movie.id
                )
            ).all()

            for credit in credits:

                # ACTOR
                if credit.credit_type == "cast":

                    actor_contribution = preferred_actors.get(
                        credit.person_id,
                        0,
                    )

                    actor_score += actor_contribution

                    if actor_contribution > 0:

                        person = db.get(
                            Person,
                            credit.person_id,
                        )

                        if person:
                            matched_actors.append(
                                person.name
                            )

                # DIRECTOR
                elif (
                    credit.credit_type == "crew"
                    and credit.job
                    and credit.job.lower()
                    == "director"
                ):

                    director_contribution = (
                        preferred_directors.get(
                            credit.person_id,
                            0,
                        )
                    )

                    director_score += director_contribution

                    if director_contribution > 0:

                        person = db.get(
                            Person,
                            credit.person_id,
                        )

                        if person:
                            matched_directors.append(
                                person.name
                            )

            # --------------------------------------------------
            # CONTENT SCORE
            # --------------------------------------------------

            content_score = (
                genre_score * 3.0
                + actor_score * 2.0
                + director_score * 3.0
            )

            # --------------------------------------------------
            # MOVIE QUALITY SIGNAL
            # --------------------------------------------------

            quality_score = 0.0

            if movie.rating is not None:

                quality_score = (
                    movie.rating * 0.15
                )

            # --------------------------------------------------
            # FINAL SCORE
            # --------------------------------------------------

            final_score = (
                content_score
                + quality_score
            )

            # --------------------------------------------------
            # REMOVE DUPLICATE EXPLANATIONS
            # --------------------------------------------------

            matched_genres = list(
                dict.fromkeys(matched_genres)
            )

            matched_actors = list(
                dict.fromkeys(matched_actors)
            )

            matched_directors = list(
                dict.fromkeys(matched_directors)
            )

            # --------------------------------------------------
            # STORE RECOMMENDATION
            # --------------------------------------------------

            recommendations.append(
                {
                    "movie": movie,
                    "score": round(
                        final_score,
                        3,
                    ),
                    "content_score": round(
                        content_score,
                        3,
                    ),
                    "quality_score": round(
                        quality_score,
                        3,
                    ),
                    "explanation": {
                        "genres": matched_genres,
                        "actors": matched_actors,
                        "directors": matched_directors,
                    },
                }
            )

        # ======================================================
        # 6. SORT
        # ======================================================

        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        # ======================================================
        # 7. RETURN TOP RESULTS
        # ======================================================

        return recommendations[:limit]