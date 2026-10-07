import json
import random
import ssl
import time
import urllib.parse
import urllib.request

from app.core.config import TMDB_API_TOKEN


TMDB_BASE_URL = "https://api.themoviedb.org/3"


class TMDBService:

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {TMDB_API_TOKEN}",
            "accept": "application/json",
            "User-Agent": "CineScope/1.0",
            "Connection": "close",
        }

        # ========================================================
        # TLS CONFIGURATION
        # ========================================================

        self.ssl_context = ssl.SSLContext(
            ssl.PROTOCOL_TLS_CLIENT
        )

        self.ssl_context.minimum_version = (
            ssl.TLSVersion.TLSv1_2
        )

        self.ssl_context.maximum_version = (
            ssl.TLSVersion.TLSv1_2
        )

        self.ssl_context.load_default_certs()

        # Explicitly use HTTP/1.1.
        self.ssl_context.set_alpn_protocols(
            ["http/1.1"]
        )

    # ============================================================
    # INTERNAL GET REQUEST
    # ============================================================

    def _get(
        self,
        endpoint: str,
        params: dict | None = None,
        retries: int = 5,
    ) -> dict:

        url = f"{TMDB_BASE_URL}{endpoint}"

        if params:

            query_string = urllib.parse.urlencode(
                params
            )

            url = f"{url}?{query_string}"

        last_error = None

        for attempt in range(
            1,
            retries + 1,
        ):

            request = urllib.request.Request(
                url=url,
                headers=self.headers,
                method="GET",
            )

            try:

                with urllib.request.urlopen(
                    request,
                    context=self.ssl_context,
                    timeout=30,
                ) as response:

                    data = response.read().decode(
                        "utf-8"
                    )

                    return json.loads(data)

            except Exception as error:

                last_error = error

                print(
                    f"TMDB request failed "
                    f"(attempt {attempt}/{retries}): "
                    f"{error}"
                )

                if attempt < retries:

                    wait_time = (
                        2 ** (attempt - 1)
                    ) + random.uniform(
                        0.2,
                        0.8,
                    )

                    print(
                        f"Retrying TMDB request "
                        f"in {wait_time:.1f}s..."
                    )

                    time.sleep(
                        wait_time
                    )

        raise last_error

    # ============================================================
    # MOVIE DETAILS
    # ============================================================

    def get_movie(
        self,
        tmdb_id: int,
    ) -> dict:

        return self._get(
            f"/movie/{tmdb_id}",
            {
                "language": "en-US",
            },
        )

    # ============================================================
    # MOVIE CREDITS
    # ============================================================

    def get_movie_credits(
        self,
        tmdb_id: int,
    ) -> dict:

        return self._get(
            f"/movie/{tmdb_id}/credits",
            {
                "language": "en-US",
            },
        )

    # ============================================================
    # POPULAR MOVIES
    # ============================================================

    def get_popular_movies(
        self,
        page: int = 1,
    ) -> dict:

        return self._get(
            "/movie/popular",
            {
                "language": "en-US",
                "page": page,
            },
        )

    # ============================================================
    # DISCOVER MOVIES
    # ============================================================

    def discover_movies(
        self,
        page: int = 1,
        sort_by: str = "popularity.desc",
        vote_count_gte: int = 50,
    ) -> dict:

        return self._get(
            "/discover/movie",
            {
                "language": "en-US",
                "page": page,
                "sort_by": sort_by,
                "include_adult": "false",
                "include_video": "false",
                "vote_count.gte": vote_count_gte,
            },
        )

    # ============================================================
    # SEARCH MOVIES
    # ============================================================

    def search_movies(
        self,
        query: str,
        page: int = 1,
    ) -> dict:

        return self._get(
            "/search/movie",
            {
                "query": query,
                "language": "en-US",
                "page": page,
                "include_adult": "false",
            },
        )

    # ============================================================
    # SIMILAR MOVIES
    # ============================================================

    def get_similar_movies(
        self,
        tmdb_id: int,
        page: int = 1,
    ) -> dict:

        return self._get(
            f"/movie/{tmdb_id}/similar",
            {
                "language": "en-US",
                "page": page,
            },
        )

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):
        pass