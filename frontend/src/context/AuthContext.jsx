import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import api from "../services/api";

const AuthContext = createContext(null);

function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchCurrentUser = async () => {
        const token = localStorage.getItem(
            "cinescope_access_token"
        );

        if (!token) {
            setUser(null);
            setLoading(false);
            return;
        }

        try {
            const response = await api.get(
                "/api/auth/me"
            );

            setUser(response.data);
        } catch (error) {
            localStorage.removeItem(
                "cinescope_access_token"
            );

            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCurrentUser();
    }, []);

    const login = (token) => {
        localStorage.setItem(
            "cinescope_access_token",
            token
        );

        return fetchCurrentUser();
    };

    const logout = () => {
        localStorage.removeItem(
            "cinescope_access_token"
        );

        setUser(null);
    };

    const value = {
        user,
        loading,
        isAuthenticated: Boolean(user),
        login,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    return useContext(AuthContext);
}

export default AuthContext;
export { AuthProvider };