from sqlalchemy.orm import Session

from app.services.semantic_search import SemanticSearchService


semantic_search_service = SemanticSearchService()


def get_semantic_analyst_context(
    db: Session,
    question: str,
    limit: int = 5,
) -> dict:

    movies = semantic_search_service.search(
        db=db,
        query=question,
        limit=limit,
    )

    results = []

    for movie in movies:
        results.append(
            {
                "movie_id": movie.id,
                "tmdb_id": movie.tmdb_id,
                "title": movie.title,
                "overview": movie.overview,
                "rating": movie.rating,
                "vote_count": movie.vote_count,
                "popularity": movie.popularity,
            }
        )

    return {
        "query": question,
        "results": results,
    }