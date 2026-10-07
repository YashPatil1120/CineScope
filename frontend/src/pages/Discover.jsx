import { useEffect, useState } from "react";

import api from "../services/api";
import MovieCard from "../components/MovieCard";

import "./Discover.css";


const GENRES = [
    {
        label: "Action",
        query: "action movies",
    },
    {
        label: "Adventure",
        query: "adventure movies",
    },
    {
        label: "Comedy",
        query: "comedy movies",
    },
    {
        label: "Drama",
        query: "drama movies",
    },
    {
        label: "Horror",
        query: "horror movies",
    },
    {
        label: "Science Fiction",
        query: "science fiction movies",
    },
    {
        label: "Fantasy",
        query: "fantasy movies",
    },
    {
        label: "Animation",
        query: "animation movies",
    },
];


function Discover() {

    // ============================================================
    // MOVIE DATA
    // ============================================================

    const [movies, setMovies] = useState([]);

    const [searchResults, setSearchResults] =
        useState([]);


    // ============================================================
    // SEARCH
    // ============================================================

    const [query, setQuery] = useState("");

    const [searching, setSearching] =
        useState(false);

    const [searchError, setSearchError] =
        useState("");

    const [hasSearched, setHasSearched] =
        useState(false);


    // ============================================================
    // CATALOG
    // ============================================================

    const [loadingMovies, setLoadingMovies] =
        useState(true);

    const [movieError, setMovieError] =
        useState("");


    // ============================================================
    // GENRE
    // ============================================================

    const [selectedGenre, setSelectedGenre] =
        useState("");


    // ============================================================
    // FETCH CATALOG
    // ============================================================

    useEffect(() => {

        const fetchMovies = async () => {

            try {

                const response = await api.get(
                    "/api/movies"
                );

                setMovies(
                    response.data
                );

            } catch (error) {

                console.error(
                    "Failed to load Discover catalog:",
                    error
                );

                setMovieError(
                    "Unable to load the movie catalog."
                );

            } finally {

                setLoadingMovies(false);

            }

        };


        fetchMovies();

    }, []);


    // ============================================================
    // SEARCH
    // ============================================================

    const handleSearch = async (
        searchQuery = query
    ) => {

        const trimmedQuery =
            searchQuery.trim();


        if (!trimmedQuery) {

            setHasSearched(false);
            setSearchResults([]);
            setSearchError("");

            return;
        }


        setSearching(true);
        setSearchError("");
        setHasSearched(true);


        try {

            const response = await api.get(
                "/api/movies/hybrid-search",
                {
                    params: {
                        q: trimmedQuery,
                        limit: 20,
                    },
                }
            );


            setSearchResults(
                response.data
            );

        } catch (error) {

            console.error(
                "Discover search failed:",
                error
            );

            setSearchError(
                "Unable to search movies."
            );

            setSearchResults([]);

        } finally {

            setSearching(false);

        }

    };


    // ============================================================
    // SEARCH SUBMIT
    // ============================================================

    const handleSubmit = (event) => {

        event.preventDefault();

        handleSearch();

    };


    // ============================================================
    // GENRE SEARCH
    // ============================================================

    const handleGenreClick = (genre) => {

        if (selectedGenre === genre.label) {

            setSelectedGenre("");
            setHasSearched(false);
            setSearchResults([]);

            return;
        }


        setSelectedGenre(
            genre.label
        );

        setQuery(
            genre.query
        );

        handleSearch(
            genre.query
        );

    };


    // ============================================================
    // CLEAR SEARCH
    // ============================================================

    const clearSearch = () => {

        setQuery("");
        setHasSearched(false);
        setSearchResults([]);
        setSearchError("");
        setSelectedGenre("");

    };


    // ============================================================
    // POPULAR MOVIES
    // ============================================================

    const popularMovies =
        movies.slice(0, 10);


    // ============================================================
    // CATALOG DISPLAY
    // ============================================================

    const catalogMovies =
        movies.slice(0, 24);


    // ============================================================
    // RENDER
    // ============================================================

    return (

        <div className="discover-page">

            {/* ==================================================
                HERO
            ================================================== */}

            <section className="discover-hero">

                <div className="discover-eyebrow">
                    CINESCOPE DISCOVERY
                </div>


                <h1>
                    Explore your next movie.
                </h1>


                <p>
                    Browse the CineScope catalog or search
                    by movie, actor, director, genre, or mood.
                </p>


                {/* ==================================================
                    SEARCH
                ================================================== */}

                <form
                    className="discover-search"
                    onSubmit={handleSubmit}
                >

                    <span className="discover-search-icon">
                        🔍
                    </span>


                    <input
                        type="text"
                        value={query}
                        onChange={(event) =>
                            setQuery(
                                event.target.value
                            )
                        }
                        placeholder="Search movies, actors, directors, genres, or moods..."
                    />


                    {query && (
                        <button
                            type="button"
                            className="discover-clear"
                            onClick={clearSearch}
                        >
                            ×
                        </button>
                    )}


                    <button
                        type="submit"
                        disabled={
                            searching ||
                            !query.trim()
                        }
                    >
                        {searching
                            ? "Searching..."
                            : "Search"}
                    </button>

                </form>

            </section>


            {/* ==================================================
                SEARCH RESULTS
            ================================================== */}

            {hasSearched && (

                <section className="discover-section">

                    <div className="discover-section-header">

                        <div>
                            <span className="discover-section-label">
                                SEARCH
                            </span>

                            <h2>
                                Results for "{query}"
                            </h2>
                        </div>


                        <button
                            className="discover-back-button"
                            onClick={clearSearch}
                        >
                            Back to Discover
                        </button>

                    </div>


                    {searching && (
                        <p className="discover-status">
                            Searching the CineScope catalog...
                        </p>
                    )}


                    {searchError && (
                        <p className="discover-status error">
                            {searchError}
                        </p>
                    )}


                    {!searching &&
                        !searchError &&
                        searchResults.length === 0 && (
                            <p className="discover-status">
                                No movies found for this search.
                            </p>
                        )}


                    {!searching &&
                        !searchError &&
                        searchResults.length > 0 && (

                            <div className="discover-grid">

                                {searchResults.map(
                                    (movie) => (
                                        <MovieCard
                                            key={movie.id}
                                            movie={movie}
                                        />
                                    )
                                )}

                            </div>

                        )}

                </section>

            )}


            {/* ==================================================
                NORMAL DISCOVER CONTENT
            ================================================== */}

            {!hasSearched && (

                <>

                    {/* ==================================================
                        POPULAR NOW
                    ================================================== */}

                    <section className="discover-section">

                        <div className="discover-section-header">

                            <div>

                                <span className="discover-section-label">
                                    CURATED FROM YOUR CATALOG
                                </span>

                                <h2>
                                    Popular Now
                                </h2>

                            </div>

                        </div>


                        {loadingMovies && (
                            <p className="discover-status">
                                Loading movies...
                            </p>
                        )}


                        {movieError && (
                            <p className="discover-status error">
                                {movieError}
                            </p>
                        )}


                        {!loadingMovies &&
                            !movieError && (

                                <div className="discover-grid popular-grid">

                                    {popularMovies.map(
                                        (movie) => (
                                            <MovieCard
                                                key={movie.id}
                                                movie={movie}
                                            />
                                        )
                                    )}

                                </div>

                            )}

                    </section>


                    {/* ==================================================
                        GENRES
                    ================================================== */}

                    <section className="discover-section genre-section">

                        <div className="discover-section-header">

                            <div>

                                <span className="discover-section-label">
                                    EXPLORE BY TASTE
                                </span>

                                <h2>
                                    Browse by Genre
                                </h2>

                            </div>

                        </div>


                        <div className="genre-list">

                            {GENRES.map(
                                (genre) => (

                                    <button
                                        key={genre.label}
                                        type="button"
                                        className={
                                            `genre-pill ${
                                                selectedGenre === genre.label
                                                    ? "active"
                                                    : ""
                                            }`
                                        }
                                        onClick={() =>
                                            handleGenreClick(
                                                genre
                                            )
                                        }
                                    >
                                        {genre.label}
                                    </button>

                                )
                            )}

                        </div>

                    </section>


                    {/* ==================================================
                        ALL MOVIES
                    ================================================== */}

                    <section className="discover-section">

                        <div className="discover-section-header">

                            <div>

                                <span className="discover-section-label">
                                    CINESCOPE CATALOG
                                </span>

                                <h2>
                                    All Movies
                                </h2>

                            </div>


                            {!loadingMovies &&
                                movies.length > 0 && (

                                    <span className="movie-count">
                                        {movies.length} movies
                                    </span>

                                )}

                        </div>


                        {loadingMovies && (
                            <p className="discover-status">
                                Loading catalog...
                            </p>
                        )}


                        {!loadingMovies &&
                            !movieError && (

                                <div className="discover-grid">

                                    {catalogMovies.map(
                                        (movie) => (
                                            <MovieCard
                                                key={movie.id}
                                                movie={movie}
                                            />
                                        )
                                    )}

                                </div>

                            )}

                    </section>

                </>

            )}

        </div>

    );

}


export default Discover;