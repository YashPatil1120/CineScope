import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../services/api";
import MovieCard from "../components/MovieCard";

import "./MyMovies.css";


function MyMovies() {

    const [watchlist, setWatchlist] = useState([]);
    const [watchedMovies, setWatchedMovies] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    const [removingMovieId, setRemovingMovieId] =
        useState(null);


    // ==========================================
    // FETCH WATCHLIST + WATCHED MOVIES
    // ==========================================

    const fetchMyMovies = async () => {

        try {

            setLoading(true);
            setError("");


            // ======================================
            // FETCH WATCHLIST
            // ======================================

            const watchlistResponse =
                await api.get(
                    "/api/watchlist"
                );


            setWatchlist(
                watchlistResponse.data
            );


            // ======================================
            // FETCH MOVIE INTERACTIONS
            // ======================================

            const interactionResponse =
                await api.get(
                    "/api/interactions"
                );


            const watched =
                interactionResponse.data.filter(
                    (movie) =>
                        movie.watched === true
                );


            setWatchedMovies(watched);


        } catch (error) {

            console.error(
                "Failed to load My Movies:",
                error
            );


            if (
                error.response?.status === 401
            ) {

                setError(
                    "Please sign in to view your movies."
                );

            } else {

                setError(
                    "Unable to load your movies."
                );

            }

        } finally {

            setLoading(false);

        }

    };


    useEffect(() => {

        fetchMyMovies();

    }, []);


    // ==========================================
    // REMOVE FROM WATCHLIST
    // ==========================================

    const handleRemove = async (
        movieId
    ) => {

        setRemovingMovieId(movieId);


        try {

            await api.delete(
                `/api/watchlist/${movieId}`
            );


            setWatchlist(
                (currentMovies) =>
                    currentMovies.filter(
                        (movie) =>
                            movie.movie_id !==
                            movieId
                    )
            );


        } catch (error) {

            console.error(
                "Failed to remove movie:",
                error
            );

        } finally {

            setRemovingMovieId(null);

        }

    };


    // ==========================================
    // LOADING
    // ==========================================

    if (loading) {

        return (
            <main className="my-movies-page">

                <div className="my-movies-status">
                    Loading your movies...
                </div>

            </main>
        );

    }


    // ==========================================
    // ERROR
    // ==========================================

    if (error) {

        return (
            <main className="my-movies-page">

                <div className="my-movies-status">
                    {error}

                </div>

                <Link
                    to="/login"
                    className="my-movies-login-link"
                >
                    Sign In
                </Link>

            </main>
        );

    }


    return (

        <main className="my-movies-page">


            {/* =====================================
                PAGE HEADER
            ===================================== */}

            <div className="my-movies-header">

                <p className="my-movies-label">
                    YOUR COLLECTION
                </p>

                <h1>
                    My Movies
                </h1>

                <p className="my-movies-description">
                    Keep track of movies you want
                    to watch and the ones you've
                    already seen.
                </p>

            </div>


            {/* =====================================
                WATCHLIST
            ===================================== */}

            <section className="my-movies-section">

                <div className="my-movies-section-header">

                    <div>

                        <p className="section-label">
                            WATCHLIST
                        </p>

                        <h2>
                            Movies to Watch
                        </h2>

                    </div>

                    <span className="movie-count">
                        {watchlist.length}
                    </span>

                </div>


                {watchlist.length === 0 ? (

                    <div className="empty-movies">

                        <p>
                            Your watchlist is empty.
                        </p>

                        <Link to="/">
                            Discover movies →
                        </Link>

                    </div>

                ) : (

                    <div className="watchlist-grid">

                        {watchlist.map((movie) => (

                            <div
                                className="watchlist-item"
                                key={movie.watchlist_id}
                            >

                                <MovieCard
                                    movie={movie}
                                />

                                <button
                                    className="remove-watchlist"
                                    type="button"
                                    onClick={() =>
                                        handleRemove(
                                            movie.movie_id
                                        )
                                    }
                                    disabled={
                                        removingMovieId ===
                                        movie.movie_id
                                    }
                                >

                                    {removingMovieId ===
                                    movie.movie_id
                                        ? "Removing..."
                                        : "Remove from Watchlist"}

                                </button>

                            </div>

                        ))}

                    </div>

                )}

            </section>


            {/* =====================================
                WATCHED
            ===================================== */}

            <section className="my-movies-section watched-section">

                <div className="my-movies-section-header">

                    <div>

                        <p className="section-label">
                            WATCHED
                        </p>

                        <h2>
                            Movies You've Seen
                        </h2>

                    </div>

                    <span className="movie-count">
                        {watchedMovies.length}
                    </span>

                </div>


                {watchedMovies.length === 0 ? (

                    <div className="empty-movies">

                        <p>
                            You haven't marked any
                            movies as watched yet.
                        </p>

                        <Link to="/">
                            Find a movie →
                        </Link>

                    </div>

                ) : (

                    <div className="watched-grid">

                        {watchedMovies.map((movie) => (

                            <div
                                className="watched-item"
                                key={movie.id}
                            >

                                <MovieCard
                                    movie={movie}
                                />


                                <div className="watched-info">

                                    <span className="watched-status">
                                        ✓ Watched
                                    </span>


                                    {movie.rating && (

                                        <span className="user-rating">
                                            ★ {movie.rating}/10
                                        </span>

                                    )}

                                </div>

                            </div>

                        ))}

                    </div>

                )}

            </section>


        </main>

    );

}


export default MyMovies;