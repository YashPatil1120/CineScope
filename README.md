<div align="center">

# 🎬 CineScope

### Discover something worth watching.

**A full-stack movie discovery platform with hybrid semantic search, explainable recommendations, taste analytics, an interactive knowledge graph, and a grounded local AI analyst.**

<br/>

![React](https://img.shields.io/badge/React_19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-384--dim-6E56CF?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Llama_3.2-000000?style=for-the-badge&logo=ollama&logoColor=white)
![TMDB](https://img.shields.io/badge/Data-TMDB-01B4E4?style=for-the-badge&logo=themoviedatabase&logoColor=white)

<br/>

<img src="docs/screenshots/home.png" alt="CineScope home page" width="900"/>

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Security Notes](#-security-notes)
- [Roadmap](#-roadmap)
- [Credits](#-credits-and-attribution)
- [Author](#-author)

---

## ✨ Overview

Most movie apps give you a list of titles. **CineScope** tries to answer better questions:

> *What should I watch if I want a psychological sci-fi film?*
> *Why would I like this movie, specifically?*
> *What does my viewing history say about my taste?*
> *How are this film, its cast, its director, and other movies connected?*

It combines **natural-language search**, **recommendations that explain themselves**, **personal tracking and analytics**, a **force-directed knowledge graph**, and an **AI analyst** that answers questions using your own data, all inside a dark, cinema-inspired interface.

---

## 🌟 Features

| | Feature | What it does |
|---|---|---|
| 🔎 | **Hybrid search** | Understands queries like `movies directed by Christopher Nolan`, `psychological sci-fi`, or `movies like Interstellar` by combining intent parsing, strict metadata filters, title matching, and semantic vector search. |
| 🎯 | **Explainable recommendations** | Every recommendation card says *why* it was suggested: matching genres, shared cast, or the same director. |
| 🍿 | **Personal collection** | Maintain a watchlist, mark movies as watched, and rate them on a 1-10 scale. |
| 📊 | **Taste analytics** | Rating distribution, favorite genres, favorite actors and directors, average score, and recently watched titles. |
| 🕸️ | **Knowledge graph** | An interactive graph linking a movie to its cast, director, genres, and semantically related films, with similarity percentages on the edges. |
| 🧠 | **AI Movie Analyst** | Ask questions like *"Why would I like Interstellar?"*. A local LLM answers using only retrieved CineScope context: your profile, the movie's metadata, semantic matches, and graph relationships. |
| 🔐 | **Authentication** | JWT-based sessions with Argon2 password hashing. Every user's data is private to their account. |
| 🎞️ | **Rich movie pages** | Posters, backdrops, synopsis, runtime, genres, director, scrollable cast, and similar titles via TMDB. |

---

## 🖼️ Screenshots

### Discover and search

<div align="center">
<img src="docs/screenshots/search-results.png" alt="Search results for movies directed by Christopher Nolan" width="900"/>
<br/><sub><b>Natural-language search</b>: "Movies directed by christopher nolan" correctly returns only his films.</sub>
</div>

<br/>

<div align="center">
<img src="docs/screenshots/discover.png" alt="Discover page" width="900"/>
<br/><sub><b>Discover</b>: browse the catalog or search by movie, actor, director, genre, or mood.</sub>
</div>

### Recommendations that explain themselves

<div align="center">
<img src="docs/screenshots/recommendations.png" alt="Personalized recommendations with reasons" width="900"/>
<br/><sub>Each card shows a <b>"Recommended because"</b> panel with the genre, cast, or director signals behind it.</sub>
</div>

### Your collection and analytics

<div align="center">
<img src="docs/screenshots/my-movies-watchlist.png" alt="My Movies watchlist" width="900"/>
<br/><sub><b>My Movies</b>: watchlist plus watched collection with personal ratings.</sub>
</div>

<br/>

<div align="center">
<img src="docs/screenshots/analytics-overview.png" alt="Analytics dashboard" width="900"/>
<br/><sub><b>Analytics</b>: collection stats, rating distribution, and favorite genres.</sub>
</div>

<br/>

<div align="center">
<img src="docs/screenshots/analytics-people.png" alt="Favorite actors and directors" width="900"/>
<br/><sub>Favorite actors and directors, derived from your watch history.</sub>
</div>

### Movie details and knowledge graph

<div align="center">
<img src="docs/screenshots/movie-details.png" alt="Movie details page" width="900"/>
<br/><sub><b>Movie details</b>: genres, synopsis, director, one-click "Mark as Watched" and 1-10 rating.</sub>
</div>

<br/>

<div align="center">
<img src="docs/screenshots/knowledge-graph.png" alt="Interactive knowledge graph" width="900"/>
<br/><sub><b>Knowledge graph</b>: related movies (with % similarity), actors, director, and genres around a single film.</sub>
</div>

### AI Movie Analyst

<div align="center">
<img src="docs/screenshots/ai-analyst-answer.png" alt="AI Movie Analyst answering a question" width="900"/>
<br/><sub>The analyst compares the movie against your actual profile, with related discoveries below the answer.</sub>
</div>

<details>
<summary><b>More screenshots</b></summary>

<br/>

<div align="center">

<img src="docs/screenshots/trending.png" alt="Trending now" width="800"/>
<br/><sub>Trending Now</sub>

<br/><br/>

<img src="docs/screenshots/my-movies-watched.png" alt="Watched movies" width="800"/>
<br/><sub>Watched movies with personal ratings</sub>

<br/><br/>

<img src="docs/screenshots/recently-watched.png" alt="Recently watched" width="800"/>
<br/><sub>Recently watched: your rating alongside the TMDB rating</sub>

<br/><br/>

<img src="docs/screenshots/cast-and-graph.png" alt="Cast and knowledge graph" width="800"/>
<br/><sub>Cast carousel and knowledge graph header</sub>

<br/><br/>

<img src="docs/screenshots/login.png" alt="Login page" width="800"/>
<br/><sub>Sign in</sub>

</div>

</details>

---

## 🧩 How It Works

CineScope's intelligence is built from a few transparent, inspectable pieces rather than a black box.

### 1. Hybrid search

A query is first **parsed for intent** (director, actor, genre, title, or free-form semantic). Explicit intents act as **strict filters**, so `movies starring Tom Holland` can never return a film he isn't in. Candidates are then ranked by combining signals:

| Signal | Weight |
|---|---|
| Semantic similarity (cosine distance over 384-dim embeddings, top 50) | `0.60` |
| Title match (exact / partial), for title-like queries | `0.35` |
| Person match (actor or director) | `0.95` |
| Genre match | `0.72` |

Movie embeddings are generated with **Sentence Transformers** (`all-MiniLM-L6-v2`) from each movie's title, overview, genres, and credits, then stored and searched in **PostgreSQL via pgvector**.

### 2. Explainable recommendations

From your **watched** movies, CineScope builds a preference profile of genres, actors, and directors, **weighted by how you rated each film**:

| Your rating | Effect on your profile |
|---|---|
| 8-10 | Strong positive (×2) |
| 6-7 | Positive (×1) |
| 5 | Neutral |
| 1-4 | Negative: those traits are discouraged |
| Watched, unrated | Positive (×1) |

Unseen movies are scored as:

```
score = genre_match × 3  +  actor_match × 2  +  director_match × 3  +  TMDB_rating × 0.15
```

Only **positively matched** traits are surfaced in the *"Recommended because"* explanation, so the reason shown always reflects a real match.

### 3. Knowledge graph

For any movie, related films are ranked by a blended relationship score, and rendered as an interactive force-directed graph (`react-force-graph-2d`):

```
relationship = semantic × 0.45  +  genre × 0.25  +  cast × 0.20  +  director × 0.10
```

### 4. Grounded AI analyst

The analyst is retrieval-grounded, not free-form chat. For each question the backend gathers context (your overview, favorite genres/actors/directors, recent watches, semantic matches, the movie's metadata, and its graph relationships), then prompts a local **Llama 3.2 (3B)** model with strict rules: use only the supplied context, never invent facts or preferences, and say so when information is insufficient.

---

## 🧰 Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite, React Router 7, Axios, Framer Motion, react-force-graph-2d, oxlint |
| **Backend** | Python, FastAPI, Uvicorn, Pydantic |
| **Database** | PostgreSQL, SQLAlchemy 2, Alembic, psycopg 3 |
| **Vector search** | pgvector, 384-dimensional embeddings |
| **Embeddings** | Sentence Transformers: `all-MiniLM-L6-v2` |
| **Auth** | JWT (PyJWT, HS256, 60-minute tokens), Argon2 password hashing |
| **AI Analyst** | Ollama + Llama 3.2 3B (local inference) |
| **Movie data** | [TMDB API](https://www.themoviedb.org/) |

---

## 🏗️ Architecture

```mermaid
flowchart TD
    UI["⚛️ React + Vite<br/>Home · Discover · My Movies · Analytics · AI Analyst · Graph"]
    API["⚡ FastAPI<br/>Auth · Search · Recommendations · Analytics · Graph · Analyst"]
    DB[("🐘 PostgreSQL + pgvector<br/>Movies · Credits · Users · Interactions · Embeddings")]
    TMDB["🎞️ TMDB API<br/>Metadata & artwork"]
    LLM["🦙 Ollama<br/>Llama 3.2 3B"]
    EMB["🔤 Sentence Transformers<br/>all-MiniLM-L6-v2"]

    UI -- "HTTP / JSON + JWT" --> API
    API --> DB
    API --> TMDB
    API --> LLM
    API --> EMB
    EMB -. "384-dim vectors" .-> DB
```

**Data model:** `users`, `movies` (with a 384-dim `embedding` column), `genres`, `movie_genres`, `people`, `movie_credits`, `watchlist`, and `user_movie_interactions` (watched flag + rating). Schema changes are managed with Alembic migrations.

---

## 📡 API Reference

Interactive docs are available at **`/docs`** (Swagger UI) when the backend is running.

| Area | Endpoints |
|---|---|
| **Auth** | `POST /api/auth/register` · `POST /api/auth/login` · `GET /api/auth/me` |
| **Movies** | `GET /api/movies` · `GET /api/movies/{id}` · `GET /api/movies/search` · `GET /api/movies/tmdb/{tmdb_id}` · `GET /api/movies/tmdb/{tmdb_id}/similar` |
| **Search** | `GET /api/movies/hybrid-search` · `GET /api/movies/semantic-search` |
| **Recommendations** | `GET /api/recommendations` |
| **Watchlist** | `GET /api/watchlist` · `POST /api/watchlist/tmdb/{tmdb_id}` · `DELETE /api/watchlist/{movie_id}` |
| **Interactions** | `GET /api/interactions` · `POST /api/interactions/tmdb/{tmdb_id}` · `PATCH /api/interactions/{movie_id}` · `DELETE /api/interactions/{movie_id}` |
| **Analytics** | `GET /api/analytics/overview` · `/ratings` · `/genres` · `/actors` · `/directors` · `/recent` |
| **Knowledge graph** | `GET /api/graph/movie/{movie_id}` |
| **AI Analyst** | `POST /api/analyst/ask` |
| **Health** | `GET /health` · `GET /health/db` |

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+ and npm
- **PostgreSQL** with the [**pgvector**](https://github.com/pgvector/pgvector) extension
- A free **[TMDB API token](https://www.themoviedb.org/settings/api)**
- *(Optional)* **[Ollama](https://ollama.com/)** for the AI Analyst

### 1. Clone

```bash
git clone https://github.com/YashPatil1120/CineScope.git
cd CineScope
```

### 2. Backend

```bash
cd backend
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env` (use the root `.env.example` as a template):

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/cinescope
TMDB_API_TOKEN=your_tmdb_api_token_here
JWT_SECRET_KEY=your_secure_jwt_secret_here
```

Create the database, enable pgvector, and run migrations:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

```bash
alembic upgrade head
```

### 3. Populate the catalog and embeddings

CineScope needs movies in its database before search and recommendations are useful. From `backend/`:

```bash
# Import movies from TMDB
python scripts/seed_tmdb.py
python scripts/expand_catalog.py        # optional: pull more pages (edit START_PAGE / END_PAGE inside)

# Generate the 384-dim embeddings that power semantic search
python scripts/generate_movie_embeddings.py
```

> The first run downloads the `all-MiniLM-L6-v2` model, so it can take a few minutes.

### 4. Start the API

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: `http://127.0.0.1:8000`  ·  Swagger docs: `http://127.0.0.1:8000/docs`

### 5. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**, create an account, and start exploring. To point the frontend at a different API, set `VITE_API_BASE_URL` in `frontend/.env`.

### 6. Optional: enable the AI Analyst

```bash
ollama pull llama3.2:3b
ollama serve
```

The backend calls Ollama at `http://localhost:11434` (configured in `backend/app/services/llm.py`). The rest of CineScope works fine without it.

---

## 🔑 Configuration

| Variable | Where | Purpose |
|---|---|---|
| `DATABASE_URL` | backend | PostgreSQL connection string. **Required.** |
| `TMDB_API_TOKEN` | backend | Authenticates requests to TMDB. **Required.** |
| `JWT_SECRET_KEY` | backend | Signs auth tokens. **Required**; use a long random value. |
| `FRONTEND_URL` | backend | Extra allowed CORS origin for a deployed frontend. Optional. |
| `CINESCOPE_ENV_FILE` | backend | Alternate env file to load (defaults to `.env`). Optional. |
| `VITE_API_BASE_URL` | frontend | API base URL (defaults to `http://127.0.0.1:8000`). |

> ⚠️ Variables prefixed with `VITE_` are bundled into browser code. Never put secrets in them.

---

## 📁 Project Structure

```text
CineScope/
├── frontend/                     # React + Vite single-page app
│   └── src/
│       ├── pages/                # Home, Discover, MyMovies, Analytics, Analyst,
│       │                         # MovieDetails, Login, Register
│       ├── components/           # MovieCard, MovieSection, MovieGraph, Navbar, Footer
│       ├── context/              # AuthContext (JWT session state)
│       └── services/api.js       # Axios client with auth interceptor
│
├── backend/                      # FastAPI application
│   ├── app/
│   │   ├── api/                  # Route modules (auth, movies, search, analyst, ...)
│   │   ├── services/             # hybrid_search, recommendation, graph, analytics,
│   │   │                         # embedding, analyst*, llm, tmdb, movie_importer
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── core/                 # config, security (JWT/Argon2), dependencies
│   │   └── db/                   # engine and session management
│   ├── alembic/                  # Database migrations
│   └── scripts/                  # TMDB seeding, catalog expansion, embedding generation
│
├── docs/screenshots/             # README images
├── .env.example
└── README.md
```

---

## 🛡️ Security Notes

- Passwords are hashed with **Argon2**; authentication uses signed **JWTs**.
- User-specific endpoints require a valid token, and data is scoped to the authenticated user.
- Never commit `.env` files, database URLs, API tokens, or JWT secrets.
- For production: use a unique `JWT_SECRET_KEY`, serve over HTTPS, and restrict CORS to your real frontend origin.
- AI-generated answers can be imperfect; the analyst is grounded in CineScope data but is still a small local model.

---

## 🗺️ Roadmap

- [ ] Public deployment of the frontend, backend, and database
- [ ] Demo account / guided demo mode
- [ ] Automated API and end-to-end tests in CI
- [ ] Configurable LLM endpoint and graceful fallback when no model is available
- [ ] Improved "similar movies" ranking using the in-house embeddings
- [ ] Short demo video / GIF walkthrough

---

## 🙌 Credits and Attribution

- **Movie data and artwork:** [The Movie Database (TMDB)](https://www.themoviedb.org/). *This product uses the TMDB API but is not endorsed or certified by TMDB.*
- **Embeddings:** [Sentence Transformers](https://www.sbert.net/)
- **Vector search:** [pgvector](https://github.com/pgvector/pgvector)
- **Local LLM runtime:** [Ollama](https://ollama.com/) with Meta's Llama 3.2
- **Frameworks:** [React](https://react.dev/), [Vite](https://vite.dev/), [FastAPI](https://fastapi.tiangolo.com/)

Posters, backdrops, and other third-party media remain subject to their respective rights and terms.

---

## 👨‍💻 Author

**Yash Patil**
Computer Science & Engineering student passionate about full-stack development, intelligent systems, and practical machine learning.

[![GitHub](https://img.shields.io/badge/GitHub-YashPatil1120-181717?style=flat&logo=github)](https://github.com/YashPatil1120)

---

<div align="center">

**Built with curiosity, code, and a love for movies. 🍿**

If CineScope impressed you, consider giving the repo a ⭐

</div>
