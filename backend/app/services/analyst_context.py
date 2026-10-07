from sqlalchemy.orm import Session

from app.services.analytics import (
    get_user_overview,
    get_favorite_genres,
    get_favorite_actors,
    get_favorite_directors,
    get_recently_watched,
)

from app.services.analyst_semantic_context import (
    get_semantic_analyst_context,
)

from app.services.analyst_movie_context import (
    get_movie_analyst_context,
)

from app.services.analyst_graph_context import (
    get_movie_graph_analyst_context,
)


def get_user_analyst_context(
    db: Session,
    user_id: int,
) -> dict:
    """
    Build structured user context for the AI Movie Analyst.
    """

    overview = get_user_overview(
        db=db,
        user_id=user_id,
    )

    favorite_genres = get_favorite_genres(
        db=db,
        user_id=user_id,
    )

    favorite_actors = get_favorite_actors(
        db=db,
        user_id=user_id,
    )

    favorite_directors = get_favorite_directors(
        db=db,
        user_id=user_id,
    )

    recently_watched = get_recently_watched(
        db=db,
        user_id=user_id,
    )

    return {
        "overview": overview,
        "favorite_genres": favorite_genres,
        "favorite_actors": favorite_actors,
        "favorite_directors": favorite_directors,
        "recently_watched": recently_watched,
    }


def get_analyst_context(
    db,
    user_id: int,
    question: str,
    movie_id: int | None = None,
) -> dict:

    context = {
        "user": get_user_analyst_context(
            db=db,
            user_id=user_id,
        ),
        "movie": None,
        "graph": None,
        "semantic": None,
    }

    if movie_id is not None:
        context["movie"] = get_movie_analyst_context(
            db=db,
            movie_id=movie_id,
        )

        context["graph"] = get_movie_graph_analyst_context(
            db=db,
            movie_id=movie_id,
        )

    context["semantic"] = get_semantic_analyst_context(
        db=db,
        question=question,
        limit=5,
    )

    return context