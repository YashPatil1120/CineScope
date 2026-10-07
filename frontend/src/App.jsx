import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import MovieDetails from "./pages/MovieDetails";
import Home from "./pages/Home";
import Login from "./pages/Login";
import MyMovies from "./pages/MyMovies";
import Register from "./pages/Register";
import Analytics from "./pages/Analytics";
import Analyst from "./pages/Analyst";
import Discover from "./pages/Discover";
import Footer from "./components/Footer";

function App() {
    return (
        <BrowserRouter>
            <Navbar />

            <main>
                <Routes>
                    <Route
                        path="/"
                        element={<Home />}
                    />

                    <Route
                        path="/discover"
                        element={<Discover />}
                    />

                    <Route
                        path="/my-movies"
                        element={<MyMovies />}
                    />

                    <Route
                        path="/analytics"
                        element={<Analytics />}
                    />

                    <Route
                        path="/analyst"
                        element={<Analyst />}
                    />
                    

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                    <Route
                        path="/register"
                        element={<Register />}
                    />

                    <Route
                        path="/movies/tmdb/:tmdbId"
                        element={<MovieDetails />}
                    />

                    <Route
                        path="/movies/:movieId"
                        element={<MovieDetails />}
                    />
                </Routes>
            </main>
        </BrowserRouter>
    );
}

export default App;