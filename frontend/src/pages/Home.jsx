import { useEffect, useState } from "react";

import MovieSection from "../components/MovieSection";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

import "./Home.css";


function Home() {

    const { isAuthenticated } = useAuth();


    // ============================================================
    // MOVIE DATA
    // ============================================================

    const [trendingMovies, setTrendingMovies] = useState([]);

    const [recommendedMovies, setRecommendedMovies] =
        useState([]);

    const [searchResults, setSearchResults] =
        useState([]);


    // ============================================================
    // SEARCH STATE
    // ============================================================

    const [query, setQuery] = useState("");

    const [searching, setSearching] =
        useState(false);

    const [searchError, setSearchError] =
        useState("");

    const [hasSearched, setHasSearched] =
        useState(false);


    // ============================================================
    // TRENDING STATE
    // ============================================================

    const [loadingTrending, setLoadingTrending] =
        useState(true);

    const [trendingError, setTrendingError] =
        useState("");


    // ============================================================
    // RECOMMENDATION STATE
    // ============================================================

    const [loadingRecommendations, setLoadingRecommendations] =
        useState(false);

    const [recommendationError, setRecommendationError] =
        useState("");


    // ============================================================
    // FETCH TRENDING MOVIES
    // ============================================================

    useEffect(() => {

        const fetchTrendingMovies = async () => {

            try {

                const response = await api.get(
                    "/api/movies"
                );

                setTrendingMovies(
                    response.data
                );

            } catch (error) {

                console.error(
                    "Failed to load trending movies:",
                    error
                );

                setTrendingError(
                    "Unable to load trending movies."
                );

            } finally {

                setLoadingTrending(false);

            }

        };


        fetchTrendingMovies();

    }, []);


    // ============================================================
    // FETCH PERSONALIZED RECOMMENDATIONS
    // ============================================================

    useEffect(() => {

        const fetchRecommendations = async () => {

            if (!isAuthenticated) {

                setRecommendedMovies([]);

                return;

            }


            setLoadingRecommendations(true);

            setRecommendationError("");


            try {

                const response = await api.get(
                    "/api/recommendations",
                    {
                        params: {
                            limit: 10,
                        },
                    }
                );


                setRecommendedMovies(
                    response.data
                );

            } catch (error) {

                console.error(
                    "Failed to load recommendations:",
                    error
                );

                setRecommendationError(
                    "Unable to load personalized recommendations."
                );

                setRecommendedMovies([]);

            } finally {

                setLoadingRecommendations(false);

            }

        };


        fetchRecommendations();

    }, [isAuthenticated]);


    // ============================================================
    // HYBRID MOVIE SEARCH
    // ============================================================
    //
    // Hybrid Search V1 supports:
    //
    // 1. Actor queries
    //    "movies starring Tom Holland"
    //
    // 2. Director queries
    //    "movies directed by Christopher Nolan"
    //
    // 3. Genre queries
    //    "action movies"
    //
    // 4. Natural-language semantic queries
    //    "lonely astronaut exploring deep space"
    //
    // 5. Title queries
    //    "Interstellar"
    //
    // The backend decides which search strategy to use.
    //
    // ============================================================

    const handleSearch = async (
        searchQuery = query
    ) => {

        const trimmedQuery =
            searchQuery.trim();


        if (!trimmedQuery) {

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
                        limit: 10,
                    },
                }
            );


            setSearchResults(
                response.data
            );

        } catch (error) {

            console.error(
                "Hybrid movie search failed:",
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
    // EXAMPLE SEARCH
    // ============================================================

    const handleExampleSearch = (
        example
    ) => {

        setQuery(example);

        handleSearch(example);

    };


    // ============================================================
    // RENDER
    // ============================================================

    return (

        <div className="home-page">


            {/* ==================================================
                HERO SECTION
            ================================================== */}

            <section className="hero">

                <div className="hero-content">


                    <p className="hero-label">
                        C I N E S C O P E
                    </p>


                    <h1>
                        Discover something
                        <br />
                        worth watching.
                    </h1>


                    <p className="hero-description">
                        Explore movies based on your mood,
                        taste, and curiosity.
                    </p>


                    {/* ==================================================
                        HYBRID SEARCH
                    ================================================== */}

                    <form
                        className="hero-search"
                        onSubmit={(event) => {

                            event.preventDefault();

                            handleSearch();

                        }}
                    >

                        <span className="search-icon">
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
                            placeholder="Search movies or describe what you want..."
                        />


                        <button
                            type="submit"
                            disabled={searching}
                        >

                            {searching
                                ? "Searching..."
                                : "Search"}

                        </button>

                    </form>


                    {/* ==================================================
                        EXAMPLE SEARCHES
                    ================================================== */}

                    <div className="search-examples">

                        <span>
                            Try:
                        </span>


                        <button
                            type="button"
                            onClick={() =>
                                handleExampleSearch(
                                    "psychological sci-fi"
                                )
                            }
                        >
                            psychological sci-fi
                        </button>


                        <button
                            type="button"
                            onClick={() =>
                                handleExampleSearch(
                                    "Interstellar"
                                )
                            }
                        >
                            movies like Interstellar
                        </button>


                        <button
                            type="button"
                            onClick={() =>
                                handleExampleSearch(
                                    "dark thrillers"
                                )
                            }
                        >
                            dark thrillers
                        </button>

                    </div>


                </div>

            </section>


            {/* ==================================================
                SEARCH LOADING
            ================================================== */}

            {searching && (

                <p className="movie-status">
                    Searching movies...
                </p>

            )}


            {/* ==================================================
                SEARCH ERROR
            ================================================== */}

            {searchError && (

                <p className="movie-status error">
                    {searchError}
                </p>

            )}


            {/* ==================================================
                SEARCH RESULTS
            ================================================== */}

            {!searching &&
                hasSearched &&
                !searchError && (

                    <MovieSection
                        title={`Search results for "${query}"`}
                        movies={searchResults}
                    />

                )}


            {/* ==================================================
                PERSONALIZED RECOMMENDATIONS
            ================================================== */}

            {!hasSearched &&
                isAuthenticated &&
                loadingRecommendations && (

                    <p className="movie-status">
                        Building your recommendations...
                    </p>

                )}


            {!hasSearched &&
                isAuthenticated &&
                recommendationError && (

                    <p className="movie-status error">
                        {recommendationError}
                    </p>

                )}


            {!hasSearched &&
                isAuthenticated &&
                !loadingRecommendations &&
                !recommendationError &&
                recommendedMovies.length > 0 && (

                    <MovieSection
                        title="Recommended For You"
                        movies={
                            recommendedMovies.map(
                                (recommendation) => ({
                                    ...recommendation.movie,
                                    recommendation:
                                        recommendation,
                                })
                            )
                        }
                    />

                )}


            {/* ==================================================
                TRENDING MOVIES
            ================================================== */}

            {!hasSearched &&
                !loadingTrending &&
                !trendingError && (

                    <MovieSection
                        title="Trending Now"
                        movies={trendingMovies}
                    />

                )}


            {/* ==================================================
                TRENDING LOADING
            ================================================== */}

            {loadingTrending && (

                <p className="movie-status">
                    Loading movies...
                </p>

            )}


            {/* ==================================================
                TRENDING ERROR
            ================================================== */}

            {trendingError && (

                <p className="movie-status error">
                    {trendingError}
                </p>

            )}


        </div>

    );

}


export default Home;