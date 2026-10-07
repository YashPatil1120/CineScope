from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.services.embedding import embedding_service


class SemanticSearchService:

    def search(
        self,
        db: Session,
        query: str,
        limit: int = 10,
    ):
        # ======================================================
        # 1. GENERATE QUERY EMBEDDING
        # ======================================================

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        # ======================================================
        # 2. SEMANTIC SIMILARITY SEARCH
        # ======================================================

        similarity_distance = (
            Movie.embedding.cosine_distance(
                query_embedding
            )
        )

        movies = db.scalars(
            select(Movie)
            .where(
                Movie.embedding.is_not(None)
            )
            .order_by(
                similarity_distance
            )
            .limit(limit)
        ).all()

        # ======================================================
        # 3. RETURN RESULTS
        # ======================================================

        return movies