import math

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.models.person import Person
from app.models.movie_credit import MovieCredit


def cosine_similarity(
    vector_a,
    vector_b,
) -> float:
    """
    Calculate cosine similarity between two vectors.

    Movie embeddings are already normalized, but we
    calculate this safely for robustness.
    """

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        return 0.0

    dot_product = sum(
        a * b
        for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def get_movie_graph(
    db: Session,
    movie_id: int,
) -> dict | None:

    # ==================================================
    # 1. MAIN MOVIE
    # ==================================================

    movie = db.scalar(
        select(Movie).where(Movie.id == movie_id)
    )

    if movie is None:
        return None

    nodes = []
    links = []

    movie_node_id = f"movie-{movie.id}"

    nodes.append(
        {
            "id": movie_node_id,
            "label": movie.title,
            "type": "movie",
            "metadata": {
                "movie_id": movie.id,
                "tmdb_id": movie.tmdb_id,
                "rating": movie.rating,
                "poster_path": movie.poster_path,
                "release_date": (
                    movie.release_date.isoformat()
                    if movie.release_date
                    else None
                ),
            },
        }
    )

    # ==================================================
    # 2. GENRES FOR MAIN MOVIE
    # ==================================================

    genre_rows = db.execute(
        select(Genre)
        .join(
            MovieGenre,
            MovieGenre.genre_id == Genre.id,
        )
        .where(
            MovieGenre.movie_id == movie.id
        )
    ).scalars().all()

    current_genre_ids = {
        genre.id
        for genre in genre_rows
    }

    for genre in genre_rows:

        genre_node_id = f"genre-{genre.id}"

        nodes.append(
            {
                "id": genre_node_id,
                "label": genre.name,
                "type": "genre",
                "metadata": {
                    "genre_id": genre.id,
                },
            }
        )

        links.append(
            {
                "source": movie_node_id,
                "target": genre_node_id,
                "relationship": "HAS_GENRE",
            }
        )

    # ==================================================
    # 3. LOAD ALL CAST + DIRECTORS
    # ==================================================

    credit_rows = db.execute(
        select(MovieCredit, Person)
        .join(
            Person,
            Person.id == MovieCredit.person_id,
        )
    ).all()

    cast_by_movie = {}
    directors_by_movie = {}

    for credit, person in credit_rows:

        if credit.credit_type == "cast":

            cast_by_movie.setdefault(
                credit.movie_id,
                set(),
            ).add(person.id)

        elif (
            credit.credit_type == "crew"
            and credit.job
            and credit.job.lower() == "director"
        ):

            directors_by_movie.setdefault(
                credit.movie_id,
                set(),
            ).add(person.id)

    # ==================================================
    # 4. CAST FOR MAIN MOVIE
    # ==================================================

    current_cast_ids = cast_by_movie.get(
        movie.id,
        set(),
    )

    main_cast_rows = db.execute(
        select(
            MovieCredit,
            Person,
        )
        .join(
            Person,
            Person.id == MovieCredit.person_id,
        )
        .where(
            MovieCredit.movie_id == movie.id,
            MovieCredit.credit_type == "cast",
        )
        .order_by(MovieCredit.id)
        .limit(8)
    ).all()

    for credit, person in main_cast_rows:

        person_node_id = f"person-{person.id}"

        nodes.append(
            {
                "id": person_node_id,
                "label": person.name,
                "type": "actor",
                "metadata": {
                    "person_id": person.id,
                    "character": credit.character_name,
                },
            }
        )

        links.append(
            {
                "source": movie_node_id,
                "target": person_node_id,
                "relationship": "ACTED_IN",
            }
        )

    # ==================================================
    # 5. DIRECTORS FOR MAIN MOVIE
    # ==================================================

    main_director_rows = db.execute(
        select(
            MovieCredit,
            Person,
        )
        .join(
            Person,
            Person.id == MovieCredit.person_id,
        )
        .where(
            MovieCredit.movie_id == movie.id,
            MovieCredit.credit_type == "crew",
            func.lower(MovieCredit.job) == "director",
        )
    ).all()

    current_director_ids = directors_by_movie.get(
        movie.id,
        set(),
    )

    for credit, person in main_director_rows:

        person_node_id = f"person-{person.id}"

        if not any(
            node["id"] == person_node_id
            for node in nodes
        ):
            nodes.append(
                {
                    "id": person_node_id,
                    "label": person.name,
                    "type": "director",
                    "metadata": {
                        "person_id": person.id,
                    },
                }
            )

        links.append(
            {
                "source": movie_node_id,
                "target": person_node_id,
                "relationship": "DIRECTED",
            }
        )

    # ==================================================
    # 6. LOAD ALL MOVIE GENRES
    # ==================================================

    movie_genre_rows = db.execute(
        select(MovieGenre)
    ).scalars().all()

    genres_by_movie = {}

    for movie_genre in movie_genre_rows:

        genres_by_movie.setdefault(
            movie_genre.movie_id,
            set(),
        ).add(movie_genre.genre_id)

    # ==================================================
    # 7. LOAD ALL MOVIES
    # ==================================================

    all_movies = db.scalars(
        select(Movie)
    ).all()

    # ==================================================
    # 8. CALCULATE INTELLIGENT RELATIONSHIPS
    # ==================================================

    scored_movies = []

    for candidate in all_movies:

        if candidate.id == movie.id:
            continue

        candidate_genres = genres_by_movie.get(
            candidate.id,
            set(),
        )

        candidate_cast = cast_by_movie.get(
            candidate.id,
            set(),
        )

        candidate_directors = directors_by_movie.get(
            candidate.id,
            set(),
        )

        # ----------------------------------------------
        # Genre similarity
        # ----------------------------------------------

        shared_genres = (
            current_genre_ids
            & candidate_genres
        )

        genre_union = (
            current_genre_ids
            | candidate_genres
        )

        genre_similarity = (
            len(shared_genres) /
            len(genre_union)
            if genre_union
            else 0.0
        )

        # ----------------------------------------------
        # Actor similarity
        # ----------------------------------------------

        shared_actors = (
            current_cast_ids
            & candidate_cast
        )

        actor_union = (
            current_cast_ids
            | candidate_cast
        )

        actor_similarity = (
            len(shared_actors) /
            len(actor_union)
            if actor_union
            else 0.0
        )

        # ----------------------------------------------
        # Director similarity
        # ----------------------------------------------

        same_director = bool(
            current_director_ids
            & candidate_directors
        )

        director_similarity = (
            1.0
            if same_director
            else 0.0
        )

        # ----------------------------------------------
        # Semantic similarity
        # ----------------------------------------------

        semantic_similarity = (
            cosine_similarity(
                movie.embedding,
                candidate.embedding,
            )
            if movie.embedding
            and candidate.embedding
            else 0.0
        )

        # ----------------------------------------------
        # Combined relationship score
        # ----------------------------------------------

        relationship_score = (
            semantic_similarity * 0.45
            + genre_similarity * 0.25
            + actor_similarity * 0.20
            + director_similarity * 0.10
        )

        # Ignore completely unrelated movies.
        if relationship_score <= 0:
            continue

        scored_movies.append(
            {
                "movie": candidate,
                "score": relationship_score,
                "shared_genres": len(
                    shared_genres
                ),
                "shared_actors": len(
                    shared_actors
                ),
                "same_director": same_director,
                "semantic_similarity": (
                    semantic_similarity
                ),
            }
        )

    # ==================================================
    # 9. TOP RELATED MOVIES
    # ==================================================

    scored_movies.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    top_related_movies = scored_movies[:6]

    # ==================================================
    # 10. CREATE RELATED MOVIE NODES
    # ==================================================

    for item in top_related_movies:

        related_movie = item["movie"]

        related_node_id = (
            f"movie-{related_movie.id}"
        )

        score_percent = round(
            item["score"] * 100,
            1,
        )

        nodes.append(
            {
                "id": related_node_id,
                "label": related_movie.title,
                "type": "related_movie",
                "metadata": {
                    "movie_id": related_movie.id,
                    "tmdb_id": related_movie.tmdb_id,
                    "rating": related_movie.rating,
                    "poster_path": (
                        related_movie.poster_path
                    ),
                    "relationship_score": (
                        score_percent
                    ),
                    "shared_genres": (
                        item["shared_genres"]
                    ),
                    "shared_actors": (
                        item["shared_actors"]
                    ),
                    "same_director": (
                        item["same_director"]
                    ),
                    "semantic_similarity": round(
                        item[
                            "semantic_similarity"
                        ],
                        3,
                    ),
                },
            }
        )

        links.append(
            {
                "source": movie_node_id,
                "target": related_node_id,
                "relationship": "RELATED_TO",
                "metadata": {
                    "score": score_percent,
                    "shared_genres": (
                        item["shared_genres"]
                    ),
                    "shared_actors": (
                        item["shared_actors"]
                    ),
                    "same_director": (
                        item["same_director"]
                    ),
                    "semantic_similarity": round(
                        item[
                            "semantic_similarity"
                        ],
                        3,
                    ),
                },
            }
        )

    # ==================================================
    # 11. RETURN GRAPH
    # ==================================================

    return {
        "movie_id": movie.id,
        "movie_title": movie.title,
        "nodes": nodes,
        "links": links,
    }