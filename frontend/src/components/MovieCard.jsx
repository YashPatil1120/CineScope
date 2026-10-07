import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";

import "./MovieCard.css";


function MovieCard({ movie }) {

    const navigate = useNavigate();

    const [addingToWatchlist, setAddingToWatchlist] =
        useState(false);

    const [watchlistAdded, setWatchlistAdded] =
        useState(false);

    const [watchlistMessage, setWatchlistMessage] =
        useState("");


    // ============================================================
    // RECOMMENDATION DATA
    // ============================================================

    const recommendation =
        movie.recommendation;

    const explanation =
        recommendation?.explanation;


    // ============================================================
    // MOVIE POSTER
    // ============================================================

    const posterUrl = movie.poster_path
        ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
        : "/placeholder-movie.jpg";


    // ============================================================
    // RELEASE YEAR
    // ============================================================

    const year = movie.release_date
        ? movie.release_date.slice(0, 4)
        : "N/A";


    // ============================================================
    // OPEN MOVIE DETAILS
    // ============================================================

    const handleClick = () => {

        if (movie.id) {

            navigate(
                `/movies/${movie.id}`
            );

            return;
        }


        if (movie.tmdb_id) {

            navigate(
                `/movies/tmdb/${movie.tmdb_id}`
            );

        }

    };


    // ============================================================
    // ADD TO WATCHLIST
    // ============================================================

    const handleAddToWatchlist = async (event) => {

        event.stopPropagation();


        if (addingToWatchlist || watchlistAdded) {
            return;
        }


        if (!movie.tmdb_id) {

            setWatchlistMessage(
                "This movie cannot be added right now."
            );

            return;
        }


        setAddingToWatchlist(true);
        setWatchlistMessage("");


        try {

            await api.post(
                `/api/watchlist/tmdb/${movie.tmdb_id}`
            );


            setWatchlistAdded(true);

            setWatchlistMessage(
                "Added to watchlist"
            );


        } catch (error) {

            console.error(
                "Failed to add movie to watchlist:",
                error
            );


            if (error.response?.status === 401) {

                setWatchlistMessage(
                    "Please log in first."
                );

            } else if (
                error.response?.status === 409
            ) {

                setWatchlistAdded(true);

                setWatchlistMessage(
                    "Already in watchlist"
                );

            } else {

                setWatchlistMessage(
                    "Unable to add movie."
                );

            }

        } finally {

            setAddingToWatchlist(false);

        }

    };


    return (

        <article
            className="movie-card"
            onClick={handleClick}
        >

            <div className="movie-poster">

                <img
                    src={posterUrl}
                    alt={`${movie.title} poster`}
                />


                <div className="movie-overlay">

                    <button
                        className={`quick-add ${
                            watchlistAdded
                                ? "added"
                                : ""
                        }`}
                        onClick={handleAddToWatchlist}
                        disabled={addingToWatchlist}
                        aria-label={
                            watchlistAdded
                                ? "Added to watchlist"
                                : "Add to watchlist"
                        }
                    >

                        {addingToWatchlist
                            ? "..."
                            : watchlistAdded
                                ? "✓"
                                : "+"}

                    </button>


                    {watchlistMessage && (

                        <span className="watchlist-message">
                            {watchlistMessage}
                        </span>

                    )}

                </div>

            </div>


            <div className="movie-info">

                <h3>
                    {movie.title}
                </h3>


                <div className="movie-meta">

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

                </div>


                {/* ==================================================
                    RECOMMENDATION EXPLANATION
                    Only appears on recommendation cards.
                ================================================== */}

                {explanation && (
                    <div
                        className="recommendation-explanation"
                        onClick={(event) =>
                            event.stopPropagation()
                        }
                    >

                        <div className="recommendation-label">
                            ✦ Recommended because
                        </div>


                        {explanation.genres?.length > 0 && (

                            <div className="recommendation-reason">
                                <span className="reason-icon">
                                    🎬
                                </span>

                                <span>
                                    You like{" "}
                                    {explanation.genres
                                        .slice(0, 2)
                                        .join(" and ")}
                                    {" "}movies
                                </span>
                            </div>

                        )}


                        {explanation.actors?.length > 0 && (

                            <div className="recommendation-reason">
                                <span className="reason-icon">
                                    ⭐
                                </span>

                                <span>
                                    Featuring{" "}
                                    {explanation.actors
                                        .slice(0, 2)
                                        .join(" and ")}
                                </span>
                            </div>

                        )}


                        {explanation.directors?.length > 0 && (

                            <div className="recommendation-reason">
                                <span className="reason-icon">
                                    🎥
                                </span>

                                <span>
                                    Directed by{" "}
                                    {explanation.directors
                                        .slice(0, 2)
                                        .join(" and ")}
                                </span>
                            </div>

                        )}

                    </div>
                )}

            </div>

        </article>

    );
}


export default MovieCard;