import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.person import Person
from app.models.movie_credit import MovieCredit

from app.services.embedding import embedding_service


class HybridSearchService:

    # ============================================================
    # QUERY UNDERSTANDING
    # ============================================================

    def _parse_query(self, query: str) -> dict:

        normalized_query = query.strip()
        lowered_query = normalized_query.lower()

        # --------------------------------------------------------
        # DIRECTOR QUERY
        # --------------------------------------------------------

        director_patterns = [
            r"movies?\s+directed\s+by\s+(.+)",
            r"films?\s+directed\s+by\s+(.+)",
            r"directed\s+by\s+(.+)",
            r"director\s+(.+)",
        ]

        for pattern in director_patterns:

            match = re.search(
                pattern,
                lowered_query,
            )

            if match:

                entity = match.group(1).strip()

                return {
                    "intent": "director",
                    "entity": entity,
                }

        # --------------------------------------------------------
        # ACTOR / CAST QUERY
        # --------------------------------------------------------

        actor_patterns = [
            r"movies?\s+starring\s+(.+)",
            r"films?\s+starring\s+(.+)",
            r"movies?\s+with\s+(.+)",
            r"films?\s+with\s+(.+)",
            r"starring\s+(.+)",
            r"cast\s+(.+)",
            r"actor\s+(.+)",
            r"actress\s+(.+)",
        ]

        for pattern in actor_patterns:

            match = re.search(
                pattern,
                lowered_query,
            )

            if match:

                entity = match.group(1).strip()

                return {
                    "intent": "actor",
                    "entity": entity,
                }

        # --------------------------------------------------------
        # GENRE QUERY
        # --------------------------------------------------------

        known_genres = {
            "action",
            "adventure",
            "animation",
            "comedy",
            "crime",
            "documentary",
            "drama",
            "family",
            "fantasy",
            "history",
            "horror",
            "music",
            "mystery",
            "romance",
            "science fiction",
            "sci-fi",
            "thriller",
            "war",
            "western",
        }

        genre_aliases = {
            "sci-fi": "science fiction",
        }

        genre_patterns = [
            r"movies?\s+in\s+the\s+(.+)\s+genre",
            r"films?\s+in\s+the\s+(.+)\s+genre",
            r"movies?\s+in\s+(.+)\s+genre",
            r"films?\s+in\s+(.+)\s+genre",
            r"(.+)\s+genre\s+movies?",
            r"(.+)\s+movies?",
        ]

        for pattern in genre_patterns:

            match = re.search(
                pattern,
                lowered_query,
            )

            if match:

                entity = match.group(1).strip()

                if entity in known_genres:

                    entity = genre_aliases.get(
                        entity,
                        entity,
                    )

                    return {
                        "intent": "genre",
                        "entity": entity,
                    }

        # --------------------------------------------------------
        # TITLE QUERY
        # --------------------------------------------------------

        words = normalized_query.split()

        if len(words) <= 5:

            return {
                "intent": "title_or_semantic",
                "entity": normalized_query,
            }

        # --------------------------------------------------------
        # GENERAL SEMANTIC QUERY
        # --------------------------------------------------------

        return {
            "intent": "semantic",
            "entity": None,
        }

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        db: Session,
        query: str,
        limit: int = 10,
    ):

        normalized_query = query.strip().lower()

        if not normalized_query:
            return []

        # ========================================================
        # QUERY UNDERSTANDING
        # ========================================================

        parsed_query = self._parse_query(
            query
        )

        intent = parsed_query["intent"]
        entity = parsed_query["entity"]

        # ========================================================
        # SCORE STORAGE
        # ========================================================

        scores = {}
        movie_lookup = {}

        # ========================================================
        # STRICT CANDIDATE FILTERING
        # ========================================================
        #
        # Actor / director / genre queries are explicit filters.
        #
        # Example:
        #
        # "movies starring Tom Holland"
        #
        # should NEVER return unrelated movies just because they
        # are semantically similar.
        #
        # The same applies to directors and genres.
        #
        # ========================================================

        candidate_ids = None

        # --------------------------------------------------------
        # ACTOR / DIRECTOR CANDIDATES
        # --------------------------------------------------------

        if intent in {
            "actor",
            "director",
        }:

            person_query = entity

            person_statement = (
                select(
                    Movie.id
                )
                .join(
                    MovieCredit,
                    MovieCredit.movie_id == Movie.id,
                )
                .join(
                    Person,
                    Person.id == MovieCredit.person_id,
                )
                .where(
                    Person.name.ilike(
                        f"%{person_query}%"
                    )
                )
            )

            if intent == "actor":

                person_statement = person_statement.where(
                    MovieCredit.credit_type == "cast"
                )

            elif intent == "director":

                person_statement = person_statement.where(
                    MovieCredit.credit_type == "crew",
                    MovieCredit.job.is_not(None),
                    MovieCredit.job.ilike("director"),
                )

            candidate_ids = set(
                db.scalars(
                    person_statement
                ).all()
            )

            # No matching person means no results.
            if not candidate_ids:
                return []

        # --------------------------------------------------------
        # GENRE CANDIDATES
        # --------------------------------------------------------

        elif intent == "genre":

            genre_query = entity

            genre_statement = (
                select(
                    Movie.id
                )
                .join(
                    MovieGenre,
                    MovieGenre.movie_id == Movie.id,
                )
                .join(
                    Genre,
                    Genre.id == MovieGenre.genre_id,
                )
                .where(
                    Genre.name.ilike(
                        f"%{genre_query}%"
                    )
                )
            )

            candidate_ids = set(
                db.scalars(
                    genre_statement
                ).all()
            )

            # No matching genre means no results.
            if not candidate_ids:
                return []

        # ========================================================
        # SEMANTIC SEARCH
        # ========================================================

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        similarity_distance = (
            Movie.embedding.cosine_distance(
                query_embedding
            )
        )

        semantic_statement = (
            select(Movie)
            .where(
                Movie.embedding.is_not(None)
            )
        )

        # --------------------------------------------------------
        # Apply strict candidate pool when necessary.
        #
        # Actor/director/genre searches only rank movies that
        # actually satisfy the explicit filter.
        # --------------------------------------------------------

        if candidate_ids is not None:

            semantic_statement = semantic_statement.where(
                Movie.id.in_(candidate_ids)
            )

        semantic_movies = db.scalars(
            semantic_statement
            .order_by(
                similarity_distance
            )
            .limit(50)
        ).all()

        # ========================================================
        # SEMANTIC SCORE
        # ========================================================

        for rank, movie in enumerate(
            semantic_movies
        ):

            movie_lookup[movie.id] = movie

            semantic_score = (
                1.0
                - (
                    rank
                    / max(
                        len(semantic_movies),
                        1,
                    )
                )
            )

            scores[movie.id] = (
                scores.get(
                    movie.id,
                    0,
                )
                + semantic_score * 0.60
            )

        # ========================================================
        # TITLE SEARCH
        # ========================================================
        #
        # Title matching is intentionally NOT used to expand
        # actor/director/genre candidate pools.
        #
        # This prevents:
        #
        # "movies starring Tom Holland"
        #
        # from accidentally returning unrelated movies.
        #
        # For normal title/semantic queries, title matching gets
        # a stronger weight.
        #
        # ========================================================

        if intent == "title_or_semantic":

            title_query = entity

            title_movies = db.scalars(
                select(Movie)
                .where(
                    Movie.title.ilike(
                        f"%{title_query}%"
                    )
                )
                .limit(50)
            ).all()

            for movie in title_movies:

                movie_lookup[movie.id] = movie

                title = movie.title.lower()

                if title == title_query.lower():

                    title_score = 1.0

                elif title_query.lower() in title:

                    title_score = 0.75

                else:

                    title_score = 0.5

                scores[movie.id] = (
                    scores.get(
                        movie.id,
                        0,
                    )
                    + title_score * 0.35
                )

        # ========================================================
        # PERSON BOOST
        # ========================================================
        #
        # At this point actor/director candidates have already
        # been strictly filtered.
        #
        # The person score therefore ranks matching movies but
        # never introduces non-matching movies.
        #
        # ========================================================

        if intent in {
            "actor",
            "director",
        }:

            person_query = entity

            person_statement = (
                select(
                    Movie,
                    MovieCredit,
                    Person,
                )
                .join(
                    MovieCredit,
                    MovieCredit.movie_id == Movie.id,
                )
                .join(
                    Person,
                    Person.id == MovieCredit.person_id,
                )
                .where(
                    Person.name.ilike(
                        f"%{person_query}%"
                    )
                )
            )

            if intent == "actor":

                person_statement = person_statement.where(
                    MovieCredit.credit_type == "cast"
                )

            elif intent == "director":

                person_statement = person_statement.where(
                    MovieCredit.credit_type == "crew",
                    MovieCredit.job.is_not(None),
                    MovieCredit.job.ilike("director"),
                )

            person_movies = db.execute(
                person_statement
            ).all()

            for (
                movie,
                credit,
                person,
            ) in person_movies:

                movie_lookup[movie.id] = movie

                person_score = 1.0

                scores[movie.id] = (
                    scores.get(
                        movie.id,
                        0,
                    )
                    + person_score * 0.95
                )

        # ========================================================
        # GENRE BOOST
        # ========================================================

        if intent == "genre":

            genre_query = entity

            genre_statement = (
                select(
                    Movie,
                    Genre,
                )
                .join(
                    MovieGenre,
                    MovieGenre.movie_id == Movie.id,
                )
                .join(
                    Genre,
                    Genre.id == MovieGenre.genre_id,
                )
                .where(
                    Genre.name.ilike(
                        f"%{genre_query}%"
                    )
                )
            )

            genre_movies = db.execute(
                genre_statement
            ).all()

            for movie, genre in genre_movies:

                # Because this is a strict genre query,
                # only matching movies should be ranked.
                if (
                    candidate_ids is not None
                    and movie.id not in candidate_ids
                ):
                    continue

                movie_lookup[movie.id] = movie

                scores[movie.id] = (
                    scores.get(
                        movie.id,
                        0,
                    )
                    + 0.90 * 0.80
                )

        # ========================================================
        # FINAL RANKING
        # ========================================================

        ranked_movies = sorted(
            movie_lookup.values(),
            key=lambda movie: scores.get(
                movie.id,
                0,
            ),
            reverse=True,
        )

        # ========================================================
        # RETURN RESULTS
        # ========================================================

        return ranked_movies[:limit]