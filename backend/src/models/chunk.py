from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

# Our embedding ai model's output limit
EMBEDDING_LIMIT = 384


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )

    page_no: Mapped[int]
    chunk_index: Mapped[int]

    text: Mapped[str] = mapped_column(Text)

    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_LIMIT))
