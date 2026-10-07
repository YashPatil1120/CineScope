import httpx

from app.core.config import TMDB_API_TOKEN


url = "https://api.themoviedb.org/3/movie/157336"

headers = {
    "Authorization": f"Bearer {TMDB_API_TOKEN}",
    "accept": "application/json",
}

response = httpx.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("TMDB connection successful!")
    print("Movie:", data["title"])
    print("TMDB ID:", data["id"])
    print("Release date:", data["release_date"])
else:
    print("TMDB request failed")
    print(response.text)