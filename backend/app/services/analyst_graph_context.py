from sqlalchemy.orm import Session

from app.services.graph import get_movie_graph


def get_movie_graph_analyst_context(
    db: Session,
    movie_id: int,
) -> dict | None:
    graph = get_movie_graph(
        db=db,
        movie_id=movie_id,
    )

    if graph is None:
        return None

    related_movies = []

    for node in graph["nodes"]:
        if node["type"] != "related_movie":
            continue

        metadata = node.get("metadata") or {}

        related_movies.append(
            {
                "movie_id": metadata.get("movie_id"),
                "tmdb_id": metadata.get("tmdb_id"),
                "title": node["label"],
                "rating": metadata.get("rating"),
                "poster_path": metadata.get("poster_path"),
                "relationship_score": metadata.get(
                    "relationship_score"
                ),
                "shared_genres": metadata.get(
                    "shared_genres",
                    0,
                ),
                "shared_actors": metadata.get(
                    "shared_actors",
                    0,
                ),
                "same_director": metadata.get(
                    "same_director",
                    False,
                ),
                "semantic_similarity": metadata.get(
                    "semantic_similarity",
                    0.0,
                ),
            }
        )

    return {
        "movie_id": graph["movie_id"],
        "movie_title": graph["movie_title"],
        "related_movies": related_movies,
    }