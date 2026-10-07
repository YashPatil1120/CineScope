from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.movie_interaction import MovieInteraction
from app.models.watchlist import Watchlist
from app.models.movie_genre import MovieGenre
from app.models.genre import Genre
from app.models.movie_credit import MovieCredit
from app.models.person import Person

def get_user_overview(
    db: Session,
    user_id: int,
) -> dict:

    # ============================================================
    # TOTAL INTERACTIONS
    # ============================================================

    total_movies = db.scalar(
        select(func.count(MovieInteraction.id))
        .where(
            MovieInteraction.user_id == user_id
        )
    ) or 0

    # ============================================================
    # WATCHED MOVIES
    # ============================================================

    watched_movies = db.scalar(
        select(func.count(MovieInteraction.id))
        .where(
            MovieInteraction.user_id == user_id,
            MovieInteraction.watched.is_(True),
        )
    ) or 0

    # ============================================================
    # RATED MOVIES
    # ============================================================

    rated_movies = db.scalar(
        select(func.count(MovieInteraction.id))
        .where(
            MovieInteraction.user_id == user_id,
            MovieInteraction.rating.is_not(None),
        )
    ) or 0

    # ============================================================
    # AVERAGE RATING
    # ============================================================

    average_rating = db.scalar(
        select(
            func.avg(
                MovieInteraction.rating
            )
        )
        .where(
            MovieInteraction.user_id == user_id,
            MovieInteraction.rating.is_not(None),
        )
    )

    if average_rating is not None:
        average_rating = round(
            float(average_rating),
            2,
        )

    # ============================================================
    # WATCHLIST COUNT
    # ============================================================

    watchlist_count = db.scalar(
        select(func.count(Watchlist.id))
        .where(
            Watchlist.user_id == user_id
        )
    ) or 0

    # ============================================================
    # RETURN
    # ============================================================

    return {
        "total_movies": total_movies,
        "watched_movies": watched_movies,
        "rated_movies": rated_movies,
        "average_rating": average_rating,
        "watchlist_count": watchlist_count,
    }

# ============================================================
# RATING DISTRIBUTION
# ============================================================

def get_rating_distribution(
    db: Session,
    user_id: int,
) -> list[dict]:

    rows = db.execute(
        select(
            MovieInteraction.rating,
            func.count(MovieInteraction.id),
        )
        .where(
            MovieInteraction.user_id == user_id,
            MovieInteraction.rating.is_not(None),
        )
        .group_by(
            MovieInteraction.rating
        )
        .order_by(
            MovieInteraction.rating
        )
    ).all()

    distribution = []

    for rating, count in rows:

        distribution.append(
            {
                "rating": rating,
                "count": count,
            }
        )

    return distribution

# ============================================================
# FAVORITE GENRES
# ============================================================

def get_favorite_genres(
    db: Session,
    user_id: int,
) -> list[dict]:

    rows = db.execute(
        select(
            Genre.name,
            func.count(
                func.distinct(
                    MovieInteraction.movie_id
                )
            ),
        )
        .join(
            MovieGenre,
            MovieGenre.genre_id == Genre.id,
        )
        .join(
            MovieInteraction,
            MovieInteraction.movie_id
            == MovieGenre.movie_id,
        )
        .where(
            MovieInteraction.user_id == user_id,
        )
        .group_by(
            Genre.id,
            Genre.name,
        )
        .order_by(
            func.count(
                func.distinct(
                    MovieInteraction.movie_id
                )
            ).desc()
        )
    ).all()

    genres = []

    for genre_name, count in rows:

        genres.append(
            {
                "genre": genre_name,
                "count": count,
            }
        )

    return genres
# ============================================================
# FAVORITE ACTORS
# ============================================================

def get_favorite_actors(
    db: Session,
    user_id: int,
) -> list[dict]:

    rows = db.execute(
        select(
            Person.name,
            func.count(
                func.distinct(
                    MovieInteraction.movie_id
                )
            ),
        )
        .join(
            MovieCredit,
            MovieCredit.person_id == Person.id,
        )
        .join(
            MovieInteraction,
            MovieInteraction.movie_id
            == MovieCredit.movie_id,
        )
        .where(
            MovieInteraction.user_id == user_id,
            MovieCredit.credit_type == "cast",
        )
        .group_by(
            Person.id,
            Person.name,
        )
        .order_by(
            func.count(
                func.distinct(
                    MovieInteraction.movie_id
                )
            ).desc()
        )
    ).all()

    actors = []

    for actor_name, count in rows:

        actors.append(
            {
                "actor": actor_name,
                "count": count,
            }
        )

    return actors

# ============================================================
# FAVORITE DIRECTORS
# ============================================================

def get_favorite_directors(
    db: Session,
    user_id: int,
) -> list[dict]:

    rows = db.execute(
        select(
            Person.name,
            func.count(
                func.distinct(
                    MovieInteraction.movie_id
                )
            ),
        )
        .join(
            MovieCredit,
            MovieCredit.person_id == Person.id,
        )
        .join(
            MovieInteraction,
            MovieInteraction.movie_id
            == MovieCredit.movie_id,
        )
        .where(
            MovieInteraction.user_id == user_id,
            MovieCredit.credit_type == "crew",
            MovieCredit.job == "Director",
        )
        .group_by(
            Person.id,
            Person.name,
        )
        .order_by(
            func.count(
                func.distinct(
                    MovieInteraction.movie_id
                )
            ).desc()
        )
    ).all()

    directors = []

    for director_name, count in rows:

        directors.append(
            {
                "director": director_name,
                "count": count,
            }
        )

    return directors

# ============================================================
# RECENTLY WATCHED
# ============================================================

def get_recently_watched(
    db: Session,
    user_id: int,
    limit: int = 10,
) -> list[dict]:

    rows = db.execute(
        select(
            Movie.id,
            Movie.title,
            Movie.poster_path,
            Movie.rating,
            MovieInteraction.rating,
            MovieInteraction.updated_at,
        )
        .join(
            MovieInteraction,
            MovieInteraction.movie_id == Movie.id,
        )
        .where(
            MovieInteraction.user_id == user_id,
            MovieInteraction.watched.is_(True),
        )
        .order_by(
            MovieInteraction.updated_at.desc()
        )
        .limit(limit)
    ).all()

    recently_watched = []

    for (
        movie_id,
        title,
        poster_path,
        movie_rating,
        user_rating,
        updated_at,
    ) in rows:

        recently_watched.append(
            {
                "movie_id": movie_id,
                "title": title,
                "poster_path": poster_path,
                "movie_rating": movie_rating,
                "user_rating": user_rating,
                "updated_at": updated_at,
            }
        )

    return recently_watched