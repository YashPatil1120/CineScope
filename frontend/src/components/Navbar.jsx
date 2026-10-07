import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

import "./Navbar.css";

function Navbar() {
    const navigate = useNavigate();

    const {
        user,
        loading,
        isAuthenticated,
        logout,
    } = useAuth();

    const handleLogout = () => {
        logout();
        navigate("/");
    };

    return (
        <nav className="navbar">
            <div className="navbar-inner">

                <Link
                    to="/"
                    className="navbar-logo"
                >
                    CINESCOPE
                </Link>


                <div className="navbar-links">

                    <Link to="/">
                        Home
                    </Link>

                    <Link to="/discover">
                        Discover
                    </Link>

                    <Link to="/my-movies">
                        My Movies
                    </Link>

                    <Link to="/analytics">
                        Analytics
                    </Link>

                    <Link to="/analyst">
                        AI Analyst
                    </Link>

                </div>


                <div className="navbar-auth">

                    {!loading &&
                        !isAuthenticated && (
                            <Link
                                to="/login"
                                className="navbar-login"
                            >
                                Sign In
                            </Link>
                        )}


                    {!loading &&
                        isAuthenticated &&
                        user && (
                            <>
                                <span className="navbar-user">

                                    <span className="navbar-user-icon">
                                        👤
                                    </span>

                                    {user.username}

                                </span>


                                <button
                                    type="button"
                                    className="navbar-logout"
                                    onClick={handleLogout}
                                >
                                    Logout
                                </button>
                            </>
                        )}

                </div>

            </div>
        </nav>
    );
}

export default Navbar;