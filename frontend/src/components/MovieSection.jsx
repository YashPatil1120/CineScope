import MovieCard from "./MovieCard";
import "./MovieSection.css";


function MovieSection({ title, movies }) {

    if (!movies || movies.length === 0) {
        return null;
    }


    return (
        <section className="movie-section">

            <div className="movie-section-header">

                <h2>
                    {title}
                </h2>

                <button
                    className="view-all"
                    type="button"
                >
                    View all →
                </button>

            </div>


            <div className="movie-grid">

                {movies.map((movie) => (
                    <MovieCard
                        key={movie.id ?? movie.tmdb_id}
                        movie={movie}
                    />
                ))}

            </div>

        </section>
    );
}


export default MovieSection;