from app.services.tmdb import TMDBService


tmdb = TMDBService()

try:
    movie = tmdb.get_movie(157336)

    print("Movie:", movie["title"])
    print("TMDB ID:", movie["id"])
    print("Runtime:", movie["runtime"])
    print("Genres:", [genre["name"] for genre in movie["genres"]])

    credits = tmdb.get_movie_credits(157336)

    print("\nCast:")
    for person in credits["cast"][:5]:
        print(
            f"- {person['name']} as {person.get('character')}"
        )

    print("\nCrew:")
    for person in credits["crew"]:
        if person["job"] == "Director":
            print(f"- Director: {person['name']}")

    popular = tmdb.get_popular_movies(1)

    print("\nPopular movies returned:", len(popular["results"]))

finally:
    tmdb.close()