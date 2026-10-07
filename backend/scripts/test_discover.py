import sys
from pathlib import Path

sys.path.append(
    str(
        Path(__file__).resolve().parents[1]
    )
)

from app.services.tmdb import TMDBService


tmdb = TMDBService()


print("Testing TMDB Discover...")


response = tmdb.discover_movies(
    page=1,
    sort_by="popularity.desc",
    vote_count_gte=50,
)


print(
    f"Page: {response.get('page')}"
)

print(
    f"Total pages: {response.get('total_pages')}"
)

print(
    f"Total results: {response.get('total_results')}"
)


movies = response.get(
    "results",
    []
)


print(
    f"Movies returned: {len(movies)}"
)


for movie in movies[:10]:

    print(
        f"{movie['id']} | "
        f"{movie['title']} | "
        f"{movie.get('release_date')} | "
        f"rating={movie.get('vote_average')} | "
        f"votes={movie.get('vote_count')}"
    )