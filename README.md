# 🎬 CineScope

### Intelligent Movie Discovery, Recommendation & Analysis Platform

CineScope is a full-stack movie discovery platform designed to go beyond traditional keyword-based movie websites.

It combines **hybrid search, semantic embeddings, personalized recommendations, user analytics, a movie knowledge graph, and a grounded AI Movie Analyst** into a single platform.

Instead of simply searching for a movie, CineScope allows users to explore movies based on **meaning, genres, actors, directors, relationships, and personal viewing behavior**.

---

## ✨ Highlights

- 🔎 **Hybrid Movie Search**
  - Keyword/title search
  - Semantic search
  - Genre-aware search
  - Actor and director filtering
  - Natural-language movie queries

- 🧠 **Semantic Search**
  - Sentence Transformer embeddings
  - 384-dimensional movie vectors
  - PostgreSQL + pgvector
  - Cosine similarity retrieval

- 🎯 **Personalized Recommendations**
  - User movie interactions
  - Watched movies
  - Ratings
  - Genres
  - Actors
  - Directors
  - Recommendation explanations

- 🕸️ **Movie Knowledge Graph**
  - Movie ↔ Actor
  - Movie ↔ Director
  - Movie ↔ Genre
  - Movie ↔ Related Movie
  - Interactive graph visualization
  - Intelligent relationship scoring

- 📊 **Personal Analytics**
  - Movies watched
  - Movies rated
  - Average rating
  - Watchlist statistics
  - Favorite genres
  - Favorite actors
  - Favorite directors
  - Recently watched movies
  - Rating distribution

- 🤖 **AI Movie Analyst**
  - Natural-language movie questions
  - User-aware context
  - Movie metadata retrieval
  - Semantic retrieval
  - Knowledge graph context
  - Local LLM inference through Ollama
  - Grounded responses based on CineScope data

- 🔐 **Authentication**
  - User registration
  - Secure password hashing
  - JWT authentication
  - Protected user-specific APIs

- 🎨 **Cinematic UI**
  - React + Vite
  - Responsive movie browsing
  - Movie cards
  - Discover page
  - Movie details
  - Interactive knowledge graph
  - Analytics dashboard
  - AI Analyst interface

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │        CineScope        │
                         │      React Frontend     │
                         └────────────┬────────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API       │
                         │       Application       │
                         └────────────┬────────────┘
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
       ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
       │ Recommendation │    │ Semantic Search │    │ Knowledge Graph│
       │    Engine      │    │     Engine     │    │     Engine     │
       └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
               │                     │                     │
               └─────────────────────┼─────────────────────┘
                                     ▼
                         ┌─────────────────────────┐
                         │      PostgreSQL         │
                         │                         │
                         │  Movies                 │
                         │  Users                  │
                         │  Genres                 │
                         │  People                 │
                         │  Credits               │
                         │  Watchlist              │
                         │  Interactions           │
                         │  Vector Embeddings      │
                         └────────────┬────────────┘
                                      │
                                      │ pgvector
                                      ▼
                         ┌─────────────────────────┐
                         │ Sentence Transformers   │
                         │ all-MiniLM-L6-v2        │
                         │ 384D Embeddings         │
                         └─────────────────────────┘

                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │      AI Analyst         │
                         │                         │
                         │ Query → Context → LLM   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │        Ollama            │
                         │       Llama 3.2 3B      │
                         └─────────────────────────┘

🔍 How CineScope Search Works
CineScope uses a hybrid retrieval approach instead of relying on a single search technique.
Example queries
Interstellar

movies directed by Christopher Nolan

movies starring Tom Holland

action movies

lonely astronaut exploring deep space

The query is analyzed and routed through the appropriate retrieval strategy.
Search components
User Query
    │
    ▼
Query Analysis
    │
    ├── Title / Keyword Matching
    │
    ├── Genre Matching
    │
    ├── Actor Matching
    │
    ├── Director Matching
    │
    └── Semantic Similarity
              │
              ▼
       Ranked Movie Results

The hybrid search system combines textual relevance, semantic similarity, and structured movie metadata.
🧠 Semantic Search
CineScope generates embeddings for movie information using:
sentence-transformers/all-MiniLM-L6-v2

Each movie receives a:
384-dimensional vector

These embeddings are stored directly in PostgreSQL using pgvector.
Semantic queries are converted into the same vector space and compared using cosine distance.
Movie Description
       │
       ▼
Sentence Transformer
       │
       ▼
384D Embedding
       │
       ▼
PostgreSQL + pgvector
       │
       ▼
Cosine Similarity
       │
       ▼
Semantically Relevant Movies

The current CineScope catalog contains:
599 movies
599 generated embeddings

🎯 Recommendation Engine
CineScope includes a personalized recommendation system based on user interactions and movie metadata.
Recommendation signals include:
- Watched movies
- User ratings
- Genres
- Actors
- Directors
- Movie similarity
Recommendations can also provide explanations such as:
You like Science Fiction and Adventure movies

or:
Featuring actors you have interacted with

or:
Directed by a director you have interacted with

This makes recommendations more interpretable instead of presenting unexplained movie results.
🕸️ Knowledge Graph
CineScope models relationships between movies and their associated entities.
                    ┌────────────┐
                    │   Actor    │
                    └─────┬──────┘
                          │
                          │ acted in
                          ▼
┌────────────┐      ┌────────────┐      ┌────────────┐
│   Genre    │─────▶│   Movie    │◀─────│  Director  │
└────────────┘      └─────┬──────┘      └────────────┘
                          │
                          │ related to
                          ▼
                    ┌────────────┐
                    │   Movie    │
                    └────────────┘

The graph is visualized interactively in the frontend.
Intelligent Movie Relationships
Related movies are ranked using a weighted relationship score:
45% Semantic Similarity
25% Genre Similarity
20% Shared Actors
10% Same Director

This allows CineScope to distinguish between movies that are merely similar by genre and movies that have multiple meaningful connections.
🤖 AI Movie Analyst
The AI Analyst allows users to interact with CineScope using natural language.
Example questions:
Why should I watch Interstellar?

What movies are similar to Interstellar?

Why is this movie recommended for me?

The important architectural principle is:
The LLM is not the source of truth.

Instead, CineScope retrieves relevant information first.
User Question
      │
      ▼
Query Analysis
      │
      ▼
Context Retrieval
      │
      ├── User Analytics
      ├── Movie Metadata
      ├── Genres
      ├── Cast
      ├── Directors
      ├── Semantic Search
      └── Knowledge Graph
      │
      ▼
Context Builder
      │
      ▼
Prompt Construction
      │
      ▼
Local LLM
      │
      ▼
Grounded Answer

This reduces the risk of the model inventing movie facts and keeps the response grounded in CineScope's retrieved data.
📊 Personal Analytics
Authenticated users receive a personalized analytics dashboard.
Current analytics include:
- Total movies
- Watched movies
- Rated movies
- Average rating
- Watchlist count
- Rating distribution
- Favorite genres
- Favorite actors
- Favorite directors
- Recently watched movies
Example:
                 CineScope Analytics

       Movies Watched        5
       Movies Rated         5
       Average Rating      7.2
       Watchlist            6

🔐 Authentication
CineScope uses JWT-based authentication.
Authentication flow:
Register
   │
   ▼
Password Hashing
   │
   ▼
PostgreSQL
   │
   ▼
Login
   │
   ▼
JWT Access Token
   │
   ▼
Authenticated API Requests

Passwords are securely hashed using Argon2 through pwdlib.
The frontend stores the access token and automatically attaches it to authenticated API requests.
🎬 Movie Data
Movie metadata is sourced from The Movie Database (TMDB).
The application uses TMDB for information such as:
- Movie titles
- Overviews
- Posters
- Backdrops
- Release dates
- Runtime
- Ratings
- Genres
- Cast
- Directors
- Similar movies
CineScope currently maintains a local catalog of:
599 movies

This allows most application functionality to operate against the local PostgreSQL database rather than requesting TMDB data for every user interaction.

CineScope/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── analytics.py
│   │   │   ├── analyst.py
│   │   │   ├── auth.py
│   │   │   ├── graph.py
│   │   │   ├── hybrid_search.py
│   │   │   ├── movies.py
│   │   │   ├── movie_interactions.py
│   │   │   ├── recommendations.py
│   │   │   ├── semantic_search.py
│   │   │   └── watchlist.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── session.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── analytics.py
│   │   │   ├── analyst.py
│   │   │   ├── analyst_context.py
│   │   │   ├── embedding.py
│   │   │   ├── graph.py
│   │   │   ├── llm.py
│   │   │   ├── movie_importer.py
│   │   │   ├── recommendations.py
│   │   │   ├── semantic_search.py
│   │   │   └── tmdb.py
│   │   │
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── scripts/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Footer.jsx
│   │   │   ├── MovieCard.jsx
│   │   │   ├── MovieGraph.jsx
│   │   │   ├── MovieSection.jsx
│   │   │   └── Navbar.jsx
│   │   │
│   │   ├── context/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Discover.jsx
│   │   │   ├── MovieDetails.jsx
│   │   │   ├── MyMovies.jsx
│   │   │   ├── Analytics.jsx
│   │   │   ├── Analyst.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
└── README.md

Local Development Setup
Prerequisites
Make sure the following are installed:
- Python 3.13+
- Node.js
- npm
- PostgreSQL
- Git
- Ollama
- GitHub account
1. Clone the Repository
git clone https://github.com/YashPatil1120/CineScope.git
cd CineScope

2. Backend Setup
Navigate to the backend:
cd backend

Create a virtual environment:
python -m venv venv

Activate it on Windows:
.\venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

3. Configure Environment Variables
Create:
backend/.env

based on:
.env.example

Example:
DATABASE_URL=postgresql://username:password@localhost:5432/cinescope
TMDB_API_TOKEN=your_tmdb_api_token_here
JWT_SECRET_KEY=your_secure_jwt_secret_here

Never commit the real .env file.
It is intentionally ignored by Git.
4. PostgreSQL Setup
Create a PostgreSQL database named:
cinescope

Then enable the pgvector extension:
CREATE EXTENSION vector;

CineScope uses pgvector for storing and querying movie embeddings.
5. Run Database Migrations
From:
backend/

run:
alembic upgrade head

Check the current migration:
alembic current

6. Start the Backend
From:
backend/

run:
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

FastAPI documentation:
http://127.0.0.1:8000/docs

7. Frontend Setup
Open another terminal:
cd frontend

Install dependencies:
npm install

Start the development server:
npm run dev

The frontend will be available at:
http://localhost:5173

🤖 AI Analyst Setup
CineScope's AI Analyst can run locally using Ollama.
Install Ollama and download the model:
ollama pull llama3.2:3b

Make sure Ollama is running.
CineScope communicates with:
http://localhost:11434

The backend uses:
llama3.2:3b

for local AI-generated explanations.
The AI Analyst retrieves CineScope context before sending the prompt to the model.
🧮 Generating Movie Embeddings
CineScope includes a script for generating movie embeddings.
From the backend directory:
python scripts/generate_movie_embeddings.py

The embedding pipeline uses:
sentence-transformers/all-MiniLM-L6-v2

and stores 384-dimensional vectors in PostgreSQL.
🔄 Movie Data Import
CineScope includes movie import functionality for retrieving movie information from TMDB and storing it locally.
The importer handles:
- Movie metadata
- Genres
- Cast
- Directors
- Existing movie detection
- Missing metadata repair
This reduces unnecessary external API calls once information already exists locally.
🧪 Production Readiness Checks
The project has been tested for:
Backend
- FastAPI startup
- API documentation
- Authentication
- Database connectivity
- PostgreSQL schema
- Alembic migrations
- pgvector extension
- Semantic search
- Hybrid search
- Recommendation APIs
- Analytics APIs
- Knowledge graph API
- AI Analyst API
Frontend
- React production build
- Routing
- Authentication flow
- Movie discovery
- Search
- Movie details
- Watchlist
- Ratings
- Analytics
- Knowledge graph
- AI Analyst
- Responsive UI
Production build:
npm run build

🔒 Security
Sensitive configuration is kept outside the repository.
Ignored files include:
.env
backend/.env
venv/
node_modules/
dist/
__pycache__/

The repository contains:
.env.example

with placeholder configuration values.
Never commit:
- API tokens
- Database passwords
- JWT secrets
- Personal credentials
📌 API Overview
Some of the major API areas include:
/api/auth
/api/movies
/api/movies/hybrid-search
/api/movies/semantic-search
/api/watchlist
/api/movie-interactions
/api/recommendations
/api/analytics
/api/graph
/api/analyst

FastAPI's interactive documentation provides the complete API specification.