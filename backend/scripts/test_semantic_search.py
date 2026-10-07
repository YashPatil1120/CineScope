import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

from app.db.session import get_session
from app.services.semantic_search import SemanticSearchService


def test_search():

    db = next(get_session())

    try:

        service = SemanticSearchService()

        query = (
            "movies starring tom holland"
        )

        results = service.search(
            db=db,
            query=query,
            limit=5,
        )

        print(
            f"\nSemantic search results for: "
            f'"{query}"\n'
        )

        for index, movie in enumerate(
            results,
            start=1,
        ):

            print(
                f"{index}. "
                f"{movie.title}"
            )

            print(
                f"   Rating: "
                f"{movie.rating}"
            )

            print(
                f"   Overview: "
                f"{movie.overview[:150] if movie.overview else 'N/A'}..."
            )

            print()

    finally:

        db.close()


if __name__ == "__main__":
    test_search()