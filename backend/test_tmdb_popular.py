import httpx

from app.core.config import TMDB_API_TOKEN


url = "https://api.themoviedb.org/3/movie/popular"

headers = {
    "Authorization": f"Bearer {TMDB_API_TOKEN}",
    "accept": "application/json",
}

params = {
    "language": "en-US",
    "page": 1,
}

response = httpx.get(
    url,
    headers=headers,
    params=params,
    timeout=30,
    trust_env=False,
)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("Popular endpoint working!")
    print("Movies returned:", len(data["results"]))

    for movie in data["results"][:5]:
        print(
            f"- {movie['title']} "
            f"(TMDB ID: {movie['id']})"
        )
else:
    print("Request failed")
    print(response.text)