from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MovieCredit(Base):
    __tablename__ = "movie_credits"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    movie_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("movies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    person_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("people.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # "cast" or "crew"
    credit_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # Used mainly for actors
    character_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Used mainly for crew
    # Example: Director, Writer, Producer
    job: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )