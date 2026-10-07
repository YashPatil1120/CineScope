from sqlalchemy.orm import Session

from app.services.analyst_context import get_analyst_context
from app.services.analyst_prompt import build_analyst_prompt
from app.services.llm import llm_service


def analyze_question(
    db: Session,
    user_id: int,
    question: str,
    movie_id: int | None = None,
):

    # ======================================================
    # 1. RETRIEVE CINESCOPE CONTEXT
    # ======================================================

    context = get_analyst_context(
        db=db,
        user_id=user_id,
        question=question,
        movie_id=movie_id,
    )

    # ======================================================
    # 2. BUILD GROUNDED PROMPT
    # ======================================================

    prompt = build_analyst_prompt(
        question=question,
        context=context,
    )

    # ======================================================
    # 3. GENERATE LLM RESPONSE
    # ======================================================

    answer = llm_service.generate(
        prompt=prompt,
    )

    # ======================================================
    # 4. TRACK WHICH CONTEXT WAS USED
    # ======================================================

    context_used = [
        "user_overview",
        "favorite_genres",
        "favorite_actors",
        "favorite_directors",
        "recently_watched",
        "semantic_retrieval",
    ]

    # ======================================================
    # 5. MOVIE CONTEXT
    # ======================================================

    movies = []

    if context["movie"] is not None:

        movies.append(
            context["movie"]["movie"]
        )

        context_used.extend(
            [
                "movie_metadata",
                "movie_genres",
                "movie_cast",
                "movie_directors",
            ]
        )

    # ======================================================
    # 6. KNOWLEDGE GRAPH CONTEXT
    # ======================================================

    if context["graph"] is not None:
        context_used.append(
            "knowledge_graph"
        )

    # ======================================================
    # 7. SEMANTIC MATCHES
    # ======================================================

    semantic_matches = []

    if context["semantic"] is not None:
        semantic_matches = (
            context["semantic"]["results"]
        )

    # ======================================================
    # 8. FINAL RESPONSE
    # ======================================================

    return {
        "answer": answer,
        "intent": "movie_analysis",
        "movies": movies,
        "semantic_matches": semantic_matches,
        "context_used": context_used,
    }