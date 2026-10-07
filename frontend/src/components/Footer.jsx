function Footer() {
    return (
        <footer className="footer">
            <div className="footer-content">

                <div className="footer-brand">
                    <span className="footer-logo">
                        CINESCOPE
                    </span>

                    <span className="footer-tagline">
                        Intelligent Movie Discovery
                    </span>
                </div>

                <div className="footer-tmdb">
                    <p>
                        This product uses the TMDB API but is not
                        endorsed or certified by TMDB.
                    </p>
                </div>

                <div className="footer-copyright">
                    © {new Date().getFullYear()} CineScope
                </div>

            </div>
        </footer>
    );
}

export default Footer;