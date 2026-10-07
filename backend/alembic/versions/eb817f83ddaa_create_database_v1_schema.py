from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eb817f83ddaa"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove the old prototype table.
    # The existing Interstellar row was only test data.
    op.drop_table("movies")

    # Movies
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tmdb_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("overview", sa.Text(), nullable=True),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.Column("poster_path", sa.String(length=500), nullable=True),
        sa.Column("backdrop_path", sa.String(length=500), nullable=True),
        sa.Column("runtime", sa.Integer(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("vote_count", sa.Integer(), nullable=True),
        sa.Column("popularity", sa.Float(), nullable=True),
        sa.Column("original_language", sa.String(length=10), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tmdb_id"),
    )

    op.create_index(
        "ix_movies_id",
        "movies",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_movies_tmdb_id",
        "movies",
        ["tmdb_id"],
        unique=False,
    )

    op.create_index(
        "ix_movies_title",
        "movies",
        ["title"],
        unique=False,
    )

    # Genres
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tmdb_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tmdb_id"),
        sa.UniqueConstraint("name"),
    )

    op.create_index(
        "ix_genres_id",
        "genres",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_genres_tmdb_id",
        "genres",
        ["tmdb_id"],
        unique=False,
    )

    # People
    op.create_table(
        "people",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tmdb_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("profile_path", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tmdb_id"),
    )

    op.create_index(
        "ix_people_id",
        "people",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_people_tmdb_id",
        "people",
        ["tmdb_id"],
        unique=False,
    )

    op.create_index(
        "ix_people_name",
        "people",
        ["name"],
        unique=False,
    )

    # Movie ↔ Genre
    op.create_table(
        "movie_genres",
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"],
            ["genres.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("movie_id", "genre_id"),
    )

    # Movie ↔ People
    op.create_table(
        "movie_credits",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("person_id", sa.Integer(), nullable=False),
        sa.Column("credit_type", sa.String(length=30), nullable=False),
        sa.Column("character_name", sa.String(length=255), nullable=True),
        sa.Column("job", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(
            ["movie_id"],
            ["movies.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["people.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_movie_credits_id",
        "movie_credits",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_movie_credits_movie_id",
        "movie_credits",
        ["movie_id"],
        unique=False,
    )

    op.create_index(
        "ix_movie_credits_person_id",
        "movie_credits",
        ["person_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("movie_credits")
    op.drop_table("movie_genres")
    op.drop_table("people")
    op.drop_table("genres")
    op.drop_table("movies")