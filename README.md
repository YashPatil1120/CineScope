::: {align="center"}
# 🎬 CineScope

### Discover something worth watching.

**An intelligent movie discovery, recommendation, and personal
film-tracking platform.**

Explore movies by title, actor, director, genre, or mood. Build a
watchlist, rate films, understand your taste, and explore connections
between movies.

![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20pgvector-4169E1?logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)

**[View the repository](https://github.com/YashPatil1120/CineScope)**
:::

------------------------------------------------------------------------

## ✨ Overview

CineScope is a full-stack movie discovery platform designed to make
finding your next film more personal and informative than browsing a
list of titles.

It brings together movie metadata, hybrid search, personalized
recommendations, watch tracking, taste analytics, semantic similarity,
an interactive knowledge graph, and an AI-powered movie analyst in one
cinematic interface.

CineScope helps answer questions such as:

-   *What should I watch if I want a psychological sci-fi film?*
-   *Which movies match my interests and ratings?*
-   *What patterns appear in my movie taste?*
-   *How are a movie, its cast, director, genres, and related films
    connected?*
-   *Why might a particular movie be a good recommendation for me?*

The application uses a dark, cinema-inspired interface with movie
artwork, recommendation explanations, and dedicated spaces for
discovery, collection management, analytics, and AI-assisted
exploration.

## 🌟 Features

### 🔎 Hybrid Movie Search

Search beyond exact titles with queries involving movies, actors,
directors, genres, and natural-language themes or moods. CineScope
combines metadata-oriented retrieval with a semantic-search layer
powered by Sentence Transformers. Movie embeddings are stored in
PostgreSQL using pgvector.

Example queries: - `Interstellar` -
`Movies directed by Christopher Nolan` - `psychological sci-fi` -
`dark thrillers` - `movies like Interstellar`

### 🎯 Personalized Recommendations

Discover films using recorded user interactions and available movie
metadata. Recommendation cards can explain suggestions through signals
such as genre affinity, shared cast, or director overlap, making results
more interpretable than an unexplained list.

Recommendation quality depends on the amount and quality of a user's
recorded interactions.

### 🍿 Personal Movie Collection

-   Maintain a watchlist of movies to watch later.
-   Track movies already watched.
-   Rate movies on a 1--10 scale.
-   Review movie artwork, titles, years, and personal ratings in one
    place.

User-specific features require an account and authentication.

### 📊 Taste Analytics

The analytics dashboard summarizes a user's recorded movie activity: -
Total movies in the collection. - Number of watched movies. - Average
personal rating. - Watchlist size. - Rating distribution. - Favorite
genres. - Frequently appearing actors and directors. - Recently watched
titles.

Analytics reflect recorded activity rather than preferences that have
not been observed.

### 🧠 AI Movie Analyst

Ask natural-language questions about movies, similarities,
recommendations, and recorded viewing preferences. The local development
setup uses **Ollama** with **Llama 3.2 (3B)** and contextual movie/user
information to ground its analysis.

The language model is a separate runtime dependency. A deployment
environment must provide a compatible inference service or gracefully
disable this feature. AI-generated answers may be inaccurate and should
not be treated as guaranteed facts.

### 🕸️ Interactive Movie Knowledge Graph

Explore relationships between: - Movies and related movies. - Actors. -
Directors. - Genres.

Connections are derived from movie metadata and similarity signals,
helping users explore a film beyond its synopsis.

### 🔐 Authentication and User Data

The backend includes JWT-based authentication and Argon2 password
hashing. User-specific interactions, watchlists, and ratings are
associated with authenticated accounts.

### 🎞️ Movie Metadata

CineScope integrates with **The Movie Database (TMDB)** for movie
metadata and artwork. Required attribution and provider terms must be
retained.

## 🖥️ Product Tour

  -----------------------------------------------------------------------
  Section                             Experience
  ----------------------------------- -----------------------------------
  **Home**                            Movie discovery, trending titles,
                                      personalized recommendations, and
                                      similar movies.

  **Discover**                        Browse the catalog and search by
                                      movie, actor, director, genre, or
                                      mood.

  **Movie details**                   View poster, backdrop, synopsis,
                                      year, rating, runtime, genres,
                                      director, and cast.

  **My Movies**                       Manage the watchlist, watched
                                      collection, and personal ratings.

  **Analytics**                       Review rating distribution,
                                      favorite genres, actors, directors,
                                      and collection statistics.

  **AI Analyst**                      Ask natural-language questions
                                      about movies and personal taste.

  **Knowledge graph**                 Explore links between a film,
                                      related titles, people, and genres.
  -----------------------------------------------------------------------

### Screenshots

To keep the README's images visible on GitHub, add your screenshots to a
repository folder such as `docs/screenshots/`, then embed them using
relative paths. Suggested gallery:

``` markdown
![CineScope Home](docs/screenshots/home.png)
![Discover](docs/screenshots/discover.png)
![Personalized Recommendations](docs/screenshots/recommendations.png)
![My Movies](docs/screenshots/my-movies.png)
![Analytics Dashboard](docs/screenshots/analytics.png)
![AI Movie Analyst](docs/screenshots/ai-analyst.png)
![Movie Details and Knowledge Graph](docs/screenshots/movie-details-graph.png)
```

## 🧰 Tech Stack

  Layer              Technologies
  ------------------ -----------------------------------------------
  Frontend           React, Vite, JavaScript, CSS
  API                Python, FastAPI, Uvicorn
  Database           PostgreSQL, SQLAlchemy, Alembic
  Vector search      pgvector, 384-dimensional sentence embeddings
  Embedding model    Sentence Transformers --- `all-MiniLM-L6-v2`
  Authentication     JWT, Argon2 password hashing
  Local AI Analyst   Ollama, Llama 3.2 3B
  Movie data         TMDB API
  Developer tools    Git, GitHub, VS Code

## 🏗️ Architecture

``` text
┌─────────────────────────────────────┐
│            React + Vite             │
│ Home · Discover · My Movies         │
│ Analytics · AI Analyst · Graph      │
└──────────────────┬──────────────────┘
                   │ HTTP / JSON
                   ▼
┌─────────────────────────────────────┐
│             FastAPI                 │
│ Auth · Movie APIs · Search          │
│ Recommendations · Analytics         │
│ User interactions · AI integration  │
└────────────┬────────────────┬───────┘
             │                │
             ▼                ▼
┌────────────────────┐  ┌──────────────────┐
│ PostgreSQL         │  │ External/local   │
│ Movie metadata     │  │ services         │
│ User data          │  │ TMDB API         │
│ Interactions       │  │ Ollama inference │
│ pgvector embeddings│  │ (local setup)    │
└────────────────────┘  └──────────────────┘
```

### Semantic search flow

1.  Movie metadata is prepared for semantic representation.
2.  `all-MiniLM-L6-v2` generates 384-dimensional embeddings.
3.  Embeddings are stored in PostgreSQL through pgvector.
4.  A search query is encoded and compared with stored representations.
5.  Semantic similarity complements keyword and metadata-based
    retrieval.

## 📁 Project Structure

The project is organized into separate frontend and backend
applications. This is a simplified overview; filenames may evolve as
development continues.

``` text
CineScope/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── ...
│   ├── alembic/
│   ├── requirements.txt
│   └── ...
├── .gitignore
├── .env.example
└── README.md
```

## ⚙️ Run Locally

### Prerequisites

-   Python 3.11+ (or the version supported by the project's
    dependencies).
-   Node.js and npm.
-   PostgreSQL with the **pgvector** extension available.
-   A TMDB API token.
-   Ollama and the configured model, if using the local AI Analyst.

> Never commit `.env`, `.env.production`, database URLs, API tokens, or
> JWT secrets to GitHub.

### 1. Clone the repository

``` bash
git clone https://github.com/YashPatil1120/CineScope.git
cd CineScope
```

### 2. Set up the backend

``` bash
cd backend
python -m venv venv
```

Activate the environment:

**Windows PowerShell**

``` powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
source venv/bin/activate
```

Install dependencies:

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a local `.env` file using `.env.example` as a reference and set
your own values:

``` dotenv
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE
TMDB_API_TOKEN=your_tmdb_api_token
JWT_SECRET_KEY=replace_with_a_long_random_secret
```

Use the database URL format expected by the installed PostgreSQL driver.
Keep real credentials private.

Make sure the database exists and enable pgvector if needed:

``` sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Run migrations from the backend directory:

``` bash
alembic upgrade head
```

> For an empty database, confirm that the migration history supports a
> clean installation before migrating. Never run destructive migration
> commands against a database containing data you need.

### 3. Start the backend

From `backend/`, with the virtual environment active:

``` bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Typical local endpoints: - API: `http://127.0.0.1:8000` - Swagger UI:
`http://127.0.0.1:8000/docs`

### 4. Set up the frontend

Open a second terminal:

``` bash
cd frontend
npm install
```

The API client defaults to `http://127.0.0.1:8000`. To override it,
create a frontend `.env` file:

``` dotenv
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the development server:

``` bash
npm run dev
```

Open the local URL printed by Vite, typically `http://localhost:5173`.

### 5. Optional: run the AI Analyst locally

Install [Ollama](https://ollama.com/) and retrieve the configured model:

``` bash
ollama pull llama3.2:3b
ollama serve
```

If Ollama is already running as a background service, you may not need
to start it manually. The backend must be configured to reach the Ollama
endpoint. A cloud host without an inference service will not
automatically support this feature.

## 🔑 Configuration

  -----------------------------------------------------------------------
  Variable                            Purpose
  ----------------------------------- -----------------------------------
  `DATABASE_URL`                      PostgreSQL connection string.

  `TMDB_API_TOKEN`                    Authenticates requests to TMDB.

  `JWT_SECRET_KEY`                    Signs and verifies authentication
                                      tokens. Use a long, random secret.

  `VITE_API_BASE_URL`                 Frontend API base URL; defaults to
                                      the local API address in the API
                                      client.

  `CINESCOPE_ENV_FILE`                Selects the environment file loaded
                                      by the backend configuration, if
                                      configured.
  -----------------------------------------------------------------------

Check `.env.example` and the current source code for any additional
variables required by your version.

**Security reminder:** Variables prefixed with `VITE_` are included in
browser-accessible frontend code. Never put secrets in them.

## 🧪 Quality Checks

**Frontend production build**

``` bash
cd frontend
npm run build
```

**Backend tests** (if the test suite is present)

``` bash
cd backend
pytest
```

**Migration checks**

``` bash
cd backend
alembic heads
alembic check
```

Run commands from the relevant project directory and activate the
backend virtual environment when needed. A successful frontend build
does not, by itself, prove that every API integration or cloud
deployment works.

## 🛡️ Security Notes

-   Never commit credentials or real `.env` files.
-   Use a unique, strong `JWT_SECRET_KEY` outside local development.
-   Restrict CORS to intended frontend origins in production.
-   Use HTTPS for public deployments.
-   Validate and authorize user-specific API operations on the backend.
-   Back up important data and avoid destructive migrations.
-   Treat AI-generated output as potentially imperfect.

## 🗺️ Roadmap

-   [ ] Complete public deployment of the frontend, backend, and
    database.
-   [ ] Add a public demo account or guided demo mode without exposing
    personal data.
-   [ ] Publish a polished screenshot gallery and short demo video.
-   [ ] Add automated API and end-to-end tests to CI.
-   [ ] Improve low-memory inference and gracefully handle an
    unavailable model service.
-   [ ] Add detailed API endpoint and data-model documentation.

## 🙌 Credits and Attribution

-   **Movie data and artwork:** [The Movie Database
    (TMDB)](https://www.themoviedb.org/). This product uses the TMDB API
    but is not endorsed or certified by TMDB. Retain required
    attribution and follow TMDB API terms.
-   **Semantic embeddings:** [Sentence
    Transformers](https://www.sbert.net/).
-   **Vector similarity storage:**
    [pgvector](https://github.com/pgvector/pgvector).
-   **Local language-model runtime:** [Ollama](https://ollama.com/).
-   **Frameworks:** [React](https://react.dev/),
    [Vite](https://vite.dev/), and
    [FastAPI](https://fastapi.tiangolo.com/).

Posters, backdrops, and other third-party media remain subject to their
respective rights and terms.

## 👨‍💻 Author

**Yash Patil**\
Computer Science & Engineering student interested in full-stack
development, intelligent systems, and practical machine learning.

-   GitHub: [@YashPatil1120](https://github.com/YashPatil1120)
-   Project repository:
    [CineScope](https://github.com/YashPatil1120/CineScope)

------------------------------------------------------------------------

::: {align="center"}
**Built with curiosity, code, and a love for movies. 🍿**

If you find the project interesting, consider giving the repository a
⭐.
:::
