import json
import ssl
import urllib.request

from app.core.config import TMDB_API_TOKEN


url = (
    "https://api.themoviedb.org/3/movie/popular"
    "?language=en-US&page=1"
)

request = urllib.request.Request(
    url,
    headers={
        "Authorization": f"Bearer {TMDB_API_TOKEN}",
        "accept": "application/json",
    },
)

context = ssl.create_default_context()

try:
    with urllib.request.urlopen(
        request,
        context=context,
        timeout=30,
    ) as response:

        data = json.loads(
            response.read().decode("utf-8")
        )

        print("Status:", response.status)
        print(
            "Movies returned:",
            len(data["results"]),
        )

        for movie in data["results"][:5]:
            print(
                f"- {movie['title']} "
                f"(TMDB ID: {movie['id']})"
            )

except Exception as error:
    print("Request failed:")
    print(type(error).__name__)
    print(error)