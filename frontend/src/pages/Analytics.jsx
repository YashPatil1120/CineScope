import { useEffect, useState } from "react";

import api from "../services/api";
import "./Analytics.css";

function Analytics() {
    const [overview, setOverview] = useState(null);
    const [ratings, setRatings] = useState([]);
    const [genres, setGenres] = useState([]);
    const [actors, setActors] = useState([]);
    const [directors, setDirectors] = useState([]);
    const [recentMovies, setRecentMovies] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                setLoading(true);
                setError("");

                const [
                    overviewResponse,
                    ratingsResponse,
                    genresResponse,
                    actorsResponse,
                    directorsResponse,
                    recentResponse,
                ] = await Promise.all([
                    api.get("/api/analytics/overview"),
                    api.get("/api/analytics/ratings"),
                    api.get("/api/analytics/genres"),
                    api.get("/api/analytics/actors"),
                    api.get("/api/analytics/directors"),
                    api.get("/api/analytics/recent"),
                ]);

                setOverview(overviewResponse.data);
                setRatings(ratingsResponse.data);
                setGenres(genresResponse.data);
                setActors(actorsResponse.data);
                setDirectors(directorsResponse.data);
                setRecentMovies(recentResponse.data);
            } catch (err) {
                console.error(
                    "Failed to load analytics:",
                    err
                );

                setError(
                    "Unable to load your analytics. Please try again."
                );
            } finally {
                setLoading(false);
            }
        };

        fetchAnalytics();
    }, []);

    if (loading) {
        return (
            <div className="analytics-page">
                <div className="analytics-loading">
                    <div className="loading-spinner"></div>
                    <p>Loading your movie journey...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="analytics-page">
                <div className="analytics-error">
                    <h2>Something went wrong</h2>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    const maxRatingCount =
        ratings.length > 0
            ? Math.max(...ratings.map((item) => item.count))
            : 1;

    const maxGenreCount =
        genres.length > 0
            ? Math.max(...genres.map((item) => item.count))
            : 1;

    const topGenres = genres.slice(0, 8);
    const topActors = actors.slice(0, 8);
    const topDirectors = directors.slice(0, 8);

    const getPosterUrl = (posterPath) => {
        if (!posterPath) {
            return null;
        }

        return `https://image.tmdb.org/t/p/w500${posterPath}`;
    };

    return (
        <div className="analytics-page">

            {/* Hero */}
            <section className="analytics-hero">
                <div className="analytics-hero-content">
                    <p className="analytics-eyebrow">
                        YOUR CINEMATIC JOURNEY
                    </p>

                    <h1>My Analytics</h1>

                    <p className="analytics-subtitle">
                        Discover what your movie choices say about
                        your taste.
                    </p>
                </div>
            </section>

            {/* Overview */}
            <section className="analytics-overview">

                <div className="stat-card">
                    <div className="stat-icon">🎬</div>

                    <div className="stat-content">
                        <span className="stat-label">
                            MOVIES
                        </span>

                        <strong>
                            {overview?.total_movies ?? 0}
                        </strong>

                        <span className="stat-description">
                            In your collection
                        </span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">👁</div>

                    <div className="stat-content">
                        <span className="stat-label">
                            WATCHED
                        </span>

                        <strong>
                            {overview?.watched_movies ?? 0}
                        </strong>

                        <span className="stat-description">
                            Movies completed
                        </span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">⭐</div>

                    <div className="stat-content">
                        <span className="stat-label">
                            AVERAGE RATING
                        </span>

                        <strong>
                            {overview?.average_rating
                                ? Number(
                                      overview.average_rating
                                  ).toFixed(1)
                                : "—"}
                        </strong>

                        <span className="stat-description">
                            Your personal score
                        </span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🔖</div>

                    <div className="stat-content">
                        <span className="stat-label">
                            WATCHLIST
                        </span>

                        <strong>
                            {overview?.watchlist_count ?? 0}
                        </strong>

                        <span className="stat-description">
                            Movies waiting for you
                        </span>
                    </div>
                </div>

            </section>

            {/* Main analytics grid */}
            <section className="analytics-grid">

                {/* Rating distribution */}
                <div className="analytics-card rating-card">

                    <div className="section-heading">
                        <div>
                            <span className="section-kicker">
                                YOUR SCORES
                            </span>

                            <h2>Rating Distribution</h2>
                        </div>
                    </div>

                    {ratings.length === 0 ? (
                        <div className="empty-state">
                            <p>
                                Start rating movies to see your
                                rating pattern.
                            </p>
                        </div>
                    ) : (
                        <div className="rating-chart">
                            {ratings.map((item) => {
                                const height =
                                    (item.count /
                                        maxRatingCount) *
                                    100;

                                return (
                                    <div
                                        className="rating-column"
                                        key={item.rating}
                                    >
                                        <span className="rating-count">
                                            {item.count}
                                        </span>

                                        <div className="rating-bar-container">
                                            <div
                                                className="rating-bar"
                                                style={{
                                                    height: `${Math.max(
                                                        height,
                                                        8
                                                    )}%`,
                                                }}
                                            ></div>
                                        </div>

                                        <span className="rating-value">
                                            {item.rating}
                                        </span>
                                    </div>
                                );
                            })}
                        </div>
                    )}

                </div>

                {/* Favorite genres */}
                <div className="analytics-card genres-card">

                    <div className="section-heading">
                        <div>
                            <span className="section-kicker">
                                YOUR TASTE
                            </span>

                            <h2>Favorite Genres</h2>
                        </div>
                    </div>

                    {topGenres.length === 0 ? (
                        <div className="empty-state">
                            <p>
                                Interact with more movies to
                                discover your favorite genres.
                            </p>
                        </div>
                    ) : (
                        <div className="genre-list">
                            {topGenres.map((genre) => (
                                <div
                                    className="genre-row"
                                    key={genre.genre}
                                >
                                    <div className="genre-info">
                                        <span className="genre-name">
                                            {genre.genre}
                                        </span>

                                        <span className="genre-count">
                                            {genre.count}
                                        </span>
                                    </div>

                                    <div className="genre-progress">
                                        <div
                                            className="genre-progress-fill"
                                            style={{
                                                width: `${
                                                    (genre.count /
                                                        maxGenreCount) *
                                                    100
                                                }%`,
                                            }}
                                        ></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                </div>

            </section>

            {/* People */}
            <section className="people-grid">

                {/* Actors */}
                <div className="analytics-card people-card">

                    <div className="section-heading">
                        <div>
                            <span className="section-kicker">
                                ON SCREEN
                            </span>

                            <h2>Favorite Actors</h2>
                        </div>
                    </div>

                    {topActors.length === 0 ? (
                        <div className="empty-state">
                            <p>No actor data available yet.</p>
                        </div>
                    ) : (
                        <div className="people-list">
                            {topActors.map((actor, index) => (
                                <div
                                    className="person-row"
                                    key={`${actor.actor}-${index}`}
                                >
                                    <span className="person-rank">
                                        {String(index + 1).padStart(
                                            2,
                                            "0"
                                        )}
                                    </span>

                                    <span className="person-name">
                                        {actor.actor}
                                    </span>

                                    <span className="person-count">
                                        {actor.count}{" "}
                                        {actor.count === 1
                                            ? "movie"
                                            : "movies"}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}

                </div>

                {/* Directors */}
                <div className="analytics-card people-card">

                    <div className="section-heading">
                        <div>
                            <span className="section-kicker">
                                BEHIND THE CAMERA
                            </span>

                            <h2>Favorite Directors</h2>
                        </div>
                    </div>

                    {topDirectors.length === 0 ? (
                        <div className="empty-state">
                            <p>
                                No director data available yet.
                            </p>
                        </div>
                    ) : (
                        <div className="people-list">
                            {topDirectors.map(
                                (director, index) => (
                                    <div
                                        className="person-row"
                                        key={`${director.director}-${index}`}
                                    >
                                        <span className="person-rank">
                                            {String(
                                                index + 1
                                            ).padStart(2, "0")}
                                        </span>

                                        <span className="person-name">
                                            {director.director}
                                        </span>

                                        <span className="person-count">
                                            {director.count}{" "}
                                            {director.count === 1
                                                ? "movie"
                                                : "movies"}
                                        </span>
                                    </div>
                                )
                            )}
                        </div>
                    )}

                </div>

            </section>

            {/* Recently watched */}
            <section className="recent-section">

                <div className="section-heading recent-heading">
                    <div>
                        <span className="section-kicker">
                            YOUR HISTORY
                        </span>

                        <h2>Recently Watched</h2>
                    </div>
                </div>

                {recentMovies.length === 0 ? (
                    <div className="analytics-card empty-recent">
                        <p>
                            Your recently watched movies will
                            appear here.
                        </p>
                    </div>
                ) : (
                    <div className="recent-movies">

                        {recentMovies.map((movie) => {
                            const posterUrl =
                                getPosterUrl(
                                    movie.poster_path
                                );

                            return (
                                <div
                                    className="recent-movie-card"
                                    key={movie.movie_id}
                                >

                                    <div className="recent-poster">
                                        {posterUrl ? (
                                            <img
                                                src={posterUrl}
                                                alt={
                                                    movie.title
                                                }
                                            />
                                        ) : (
                                            <div className="poster-placeholder">
                                                No Poster
                                            </div>
                                        )}

                                        <div className="poster-overlay">
                                            <span>
                                                ★{" "}
                                                {movie.user_rating ??
                                                    "—"}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="recent-movie-info">
                                        <h3>
                                            {movie.title}
                                        </h3>

                                        <div className="movie-meta">
                                            <span>
                                                Your rating:{" "}
                                                <strong>
                                                    {movie.user_rating ??
                                                        "—"}
                                                </strong>
                                            </span>

                                            <span>
                                                TMDB:{" "}
                                                <strong>
                                                    {movie.movie_rating
                                                        ? Number(
                                                              movie.movie_rating
                                                          ).toFixed(
                                                              1
                                                          )
                                                        : "—"}
                                                </strong>
                                            </span>
                                        </div>
                                    </div>

                                </div>
                            );
                        })}

                    </div>
                )}

            </section>

        </div>
    );
}

export default Analytics;