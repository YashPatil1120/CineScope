import { useState } from "react";
import api from "../services/api";

import "./Analyst.css";

function Analyst() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [movies, setMovies] = useState([]);
    const [semanticMatches, setSemanticMatches] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleSubmit = async (event) => {
        event.preventDefault();

        const trimmedQuestion = question.trim();

        if (!trimmedQuestion) {
            return;
        }

        setLoading(true);
        setError("");
        setAnswer("");
        setMovies([]);
        setSemanticMatches([]);

        try {
            const response = await api.post(
                "/api/analyst/ask",
                {
                    question: trimmedQuestion,
                }
            );

            setAnswer(response.data.answer || "");
            setMovies(response.data.movies || []);
            setSemanticMatches(
                response.data.semantic_matches || []
            );
        } catch (err) {
            console.error("Analyst request failed:", err);

            setError(
                err.response?.data?.detail ||
                "Unable to connect to the AI Movie Analyst."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="analyst-page">

            <section className="analyst-hero">

                <div className="analyst-eyebrow">
                    CINESCOPE INTELLIGENCE
                </div>

                <h1>
                    AI Movie Analyst
                </h1>

                <p>
                    Ask CineScope about movies, recommendations,
                    similarities, and your personal movie taste.
                </p>

            </section>


            <section className="analyst-panel">

                <form
                    className="analyst-form"
                    onSubmit={handleSubmit}
                >

                    <textarea
                        value={question}
                        onChange={(event) =>
                            setQuestion(event.target.value)
                        }
                        placeholder="Ask something like: Why would I like Interstellar?"
                        rows={4}
                        maxLength={1000}
                        disabled={loading}
                    />

                    <div className="analyst-form-footer">

                        <span>
                            {question.length}/1000
                        </span>

                        <button
                            type="submit"
                            disabled={
                                loading ||
                                !question.trim()
                            }
                        >
                            {loading
                                ? "Analyzing..."
                                : "Ask CineScope"}
                        </button>

                    </div>

                </form>


                {error && (
                    <div className="analyst-error">
                        {error}
                    </div>
                )}


                {loading && (
                    <div className="analyst-loading">
                        <div className="analyst-loading-dot" />
                        <span>
                            CineScope is analyzing your movie data...
                        </span>
                    </div>
                )}


                {answer && !loading && (
                    <section className="analyst-answer-section">

                        <div className="analyst-section-label">
                            ANALYSIS
                        </div>

                        <div className="analyst-answer">
                            {answer}
                        </div>

                    </section>
                )}


                {movies.length > 0 && !loading && (
                    <section className="analyst-results">

                        <div className="analyst-section-label">
                            MOVIE CONTEXT
                        </div>

                        <div className="analyst-movie-list">

                            {movies.map((movie) => (
                                <div
                                    className="analyst-movie-card"
                                    key={movie.id}
                                >

                                    <div>
                                        <h3>
                                            {movie.title}
                                        </h3>

                                        <p>
                                            {movie.overview}
                                        </p>
                                    </div>

                                    <div className="analyst-movie-rating">
                                        ★ {movie.rating?.toFixed(1)}
                                    </div>

                                </div>
                            ))}

                        </div>

                    </section>
                )}


                {semanticMatches.length > 0 && !loading && (
                    <section className="analyst-results">

                        <div className="analyst-section-label">
                            RELATED DISCOVERIES
                        </div>

                        <div className="analyst-semantic-list">

                            {semanticMatches.map((movie) => (
                                <div
                                    className="analyst-semantic-item"
                                    key={movie.movie_id}
                                >
                                    <span>
                                        {movie.title}
                                    </span>

                                    <span>
                                        ★ {movie.rating?.toFixed(1)}
                                    </span>
                                </div>
                            ))}

                        </div>

                    </section>
                )}

            </section>

        </div>
    );
}

export default Analyst;