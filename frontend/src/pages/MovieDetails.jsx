import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import api from "../services/api";
import MovieSection from "../components/MovieSection";
import MovieGraph from "../components/MovieGraph";
import { useAuth } from "../context/AuthContext";

import "./MovieDetails.css";


function MovieDetails() {
    const { movieId, tmdbId } = useParams();
    const navigate = useNavigate();

    const { isAuthenticated } = useAuth();

    const [movie, setMovie] = useState(null);
    const [similarMovies, setSimilarMovies] = useState([]);

    const [interaction, setInteraction] = useState(null);
    const [interactionLoading, setInteractionLoading] =
        useState(false);
    const [interactionError, setInteractionError] =
        useState("");

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");


    useEffect(() => {

        const fetchMovie = async () => {

            try {

                let response;


                // ==========================================
                // FETCH MOVIE DETAILS
                // ==========================================

                if (tmdbId) {

                    response = await api.get(
                        `/api/movies/tmdb/${tmdbId}`
                    );

                } else {

                    response = await api.get(
                        `/api/movies/${movieId}`
                    );

                }


                const movieData = response.data;

                setMovie(movieData);


                // ==========================================
                // DETERMINE TMDB ID
                // ==========================================

                const currentTmdbId =
                    tmdbId || movieData.tmdb_id;


                // ==========================================
                // FETCH USER INTERACTION
                // ==========================================

                if (isAuthenticated) {

                    try {

                        const interactionResponse =
                            await api.get(
                                "/api/interactions"
                            );


                        const existingInteraction =
                            interactionResponse.data.find(
                                (item) =>
                                    item.tmdb_id ===
                                    Number(currentTmdbId)
                            );


                        setInteraction(
                            existingInteraction || null
                        );

                    } catch (interactionError) {

                        console.error(
                            "Failed to fetch movie interaction:",
                            interactionError
                        );

                        setInteraction(null);

                    }

                } else {

                    setInteraction(null);

                }


                // ==========================================
                // FETCH SIMILAR MOVIES
                // ==========================================

                if (currentTmdbId) {

                    try {

                        const similarResponse =
                            await api.get(
                                `/api/movies/tmdb/${currentTmdbId}/similar`
                            );


                        setSimilarMovies(
                            similarResponse.data.results.slice(
                                0,
                                10
                            )
                        );

                    } catch (similarError) {

                        console.error(
                            "Failed to fetch similar movies:",
                            similarError
                        );

                        setSimilarMovies([]);

                    }

                } else {

                    setSimilarMovies([]);

                }

            } catch (err) {

                console.error(
                    "Failed to fetch movie:",
                    err
                );

                setError(
                    "Unable to load movie details."
                );

            } finally {

                setLoading(false);

            }

        };


        fetchMovie();

    }, [movieId, tmdbId, isAuthenticated]);


    // ==========================================
    // WATCHED TOGGLE
    // ==========================================

    const handleWatchedToggle = async () => {

        if (!isAuthenticated) {
            navigate("/login");
            return;
        }

        if (!movie?.tmdb_id) {
            return;
        }


        setInteractionLoading(true);
        setInteractionError("");


        try {

            // No interaction exists yet
            if (!interaction) {

                const response = await api.post(
                    `/api/interactions/tmdb/${movie.tmdb_id}`,
                    {
                        watched: true,
                        rating: null,
                    }
                );


                setInteraction(response.data);

            } else {

                // Interaction already exists
                const response = await api.patch(
                    `/api/interactions/${interaction.movie_id}`,
                    {
                        watched: !interaction.watched,
                    }
                );


                setInteraction(response.data);

            }

        } catch (error) {

            console.error(
                "Failed to update watched status:",
                error
            );

            setInteractionError(
                "Unable to update watched status."
            );

        } finally {

            setInteractionLoading(false);

        }

    };


    // ==========================================
    // RATING
    // ==========================================

    const handleRating = async (rating) => {

        if (!isAuthenticated) {
            navigate("/login");
            return;
        }

        if (!movie?.tmdb_id) {
            return;
        }


        setInteractionLoading(true);
        setInteractionError("");


        try {

            // No interaction exists yet
            if (!interaction) {

                const response = await api.post(
                    `/api/interactions/tmdb/${movie.tmdb_id}`,
                    {
                        watched: false,
                        rating,
                    }
                );


                setInteraction(response.data);

            } else {

                // Update existing interaction
                const response = await api.patch(
                    `/api/interactions/${interaction.movie_id}`,
                    {
                        rating,
                    }
                );


                setInteraction(response.data);

            }

        } catch (error) {

            console.error(
                "Failed to update rating:",
                error
            );

            setInteractionError(
                "Unable to update rating."
            );

        } finally {

            setInteractionLoading(false);

        }

    };


    // ==========================================
    // LOADING
    // ==========================================

    if (loading) {

        return (
            <div className="movie-details-status">
                Loading movie...
            </div>
        );

    }


    // ==========================================
    // ERROR
    // ==========================================

    if (error || !movie) {

        return (
            <div className="movie-details-status">
                {error || "Movie not found."}
            </div>
        );

    }


    // ==========================================
    // IMAGE URLS
    // ==========================================

    const posterUrl = movie.poster_path
        ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
        : "";


    const backdropUrl = movie.backdrop_path
        ? `https://image.tmdb.org/t/p/original${movie.backdrop_path}`
        : "";


    // ==========================================
    // META
    // ==========================================

    const year = movie.release_date
        ? movie.release_date.slice(0, 4)
        : "N/A";


    const runtimeHours = movie.runtime
        ? Math.floor(movie.runtime / 60)
        : 0;


    const runtimeMinutes = movie.runtime
        ? movie.runtime % 60
        : 0;


    return (
        <div className="movie-details-page">

            {/* =====================================
                BACKDROP
            ===================================== */}

            <div
                className="movie-backdrop"
                style={{
                    backgroundImage: `
                        linear-gradient(
                            to bottom,
                            rgba(7, 7, 10, 0.25),
                            rgba(7, 7, 10, 0.95)
                        ),
                        url(${backdropUrl})
                    `,
                }}
            />


            {/* =====================================
                BACK BUTTON
            ===================================== */}

            <button
                className="back-button"
                onClick={() => navigate(-1)}
            >
                ← Back
            </button>


            <main className="movie-details-content">

                {/* =================================
                    HERO
                ================================= */}

                <div className="movie-details-hero">

                    <div className="details-poster">

                        <img
                            src={posterUrl}
                            alt={`${movie.title} poster`}
                        />

                    </div>


                    <div className="details-info">

                        <p className="details-label">
                            C I N E S C O P E
                        </p>


                        <h1>
                            {movie.title}
                        </h1>


                        <div className="details-meta">

                            <span>
                                {year}
                            </span>

                            <span>
                                •
                            </span>

                            <span>
                                ⭐{" "}
                                {movie.rating?.toFixed(1) ?? "N/A"}
                            </span>


                            {movie.runtime && (
                                <>
                                    <span>
                                        •
                                    </span>

                                    <span>

                                        {runtimeHours > 0 &&
                                            `${runtimeHours}h `}

                                        {runtimeMinutes}m

                                    </span>
                                </>
                            )}

                        </div>


                        {/* GENRES */}

                        <div className="genre-list">

                            {movie.genres.map((genre) => (

                                <span
                                    className="genre-tag"
                                    key={genre.id}
                                >
                                    {genre.name}
                                </span>

                            ))}

                        </div>


                        {/* OVERVIEW */}

                        <p className="movie-overview">
                            {movie.overview ||
                                "No overview available."}
                        </p>


                        {/* DIRECTOR */}

                        {movie.directors.length > 0 && (

                            <div className="director-info">

                                <span className="info-label">
                                    Director
                                </span>

                                <span className="info-value">

                                    {movie.directors
                                        .map(
                                            (director) =>
                                                director.person.name
                                        )
                                        .join(", ")}

                                </span>

                            </div>

                        )}


                        {/* =================================
                            PERSONAL MOVIE ACTIONS
                        ================================= */}

                        <div className="movie-personal-actions">

                            <button
                                type="button"
                                className={`watched-button ${
                                    interaction?.watched
                                        ? "watched"
                                        : ""
                                }`}
                                onClick={handleWatchedToggle}
                                disabled={interactionLoading}
                            >

                                {interaction?.watched
                                    ? "✓ Watched"
                                    : "○ Mark as Watched"}

                            </button>


                            <div className="rating-control">

                                <span className="rating-label">
                                    Your Rating
                                </span>

                                <div className="rating-buttons">

                                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(
                                        (rating) => (

                                            <button
                                                key={rating}
                                                type="button"
                                                className={`rating-button ${
                                                    interaction?.rating ===
                                                    rating
                                                        ? "selected"
                                                        : ""
                                                }`}
                                                onClick={() =>
                                                    handleRating(
                                                        rating
                                                    )
                                                }
                                                disabled={
                                                    interactionLoading
                                                }
                                                aria-label={`Rate ${rating} out of 10`}
                                            >
                                                {rating}
                                            </button>

                                        )
                                    )}

                                </div>

                            </div>


                            {interactionError && (

                                <p className="interaction-error">
                                    {interactionError}
                                </p>

                            )}

                        </div>

                    </div>

                </div>


                {/* =================================
                    CAST
                ================================= */}

                {movie.cast.length > 0 && (

                    <section className="cast-section">

                        <div className="details-section-header">

                            <h2>
                                Cast
                            </h2>

                        </div>


                        <div className="cast-row">

                            {movie.cast.map((actor) => {

                                const profileUrl =
                                    actor.person.profile_path
                                        ? `https://image.tmdb.org/t/p/w185${actor.person.profile_path}`
                                        : "";


                                return (

                                    <article
                                        className="cast-card"
                                        key={actor.person.id}
                                    >

                                        <div className="cast-image">

                                            {profileUrl ? (

                                                <img
                                                    src={profileUrl}
                                                    alt={actor.person.name}
                                                />

                                            ) : (

                                                <div className="cast-placeholder">
                                                    ?
                                                </div>

                                            )}

                                        </div>


                                        <h3>
                                            {actor.person.name}
                                        </h3>


                                        <p>
                                            {actor.character_name ||
                                                "Unknown role"}
                                        </p>

                                    </article>

                                );

                            })}

                        </div>

                    </section>

                )}

                {/* =================================
                KNOWLEDGE GRAPH
                ================================= */}

                {movie.id && (
                    <MovieGraph
                        movieId={movie.id}
                    />
                )}


                {/* =================================
                    SIMILAR MOVIES
                ================================= */}

                {similarMovies.length > 0 && (

                    <MovieSection
                        title="Similar Movies"
                        movies={similarMovies}
                    />

                )}

            </main>

        </div>
    );
}


export default MovieDetails;