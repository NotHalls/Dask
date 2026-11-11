from sqlalchemy import select
from sqlalchemy.orm import Session

from models.chunk import Chunk
from models.document import Document
from services.embeddings import embed_texts


def search_chunks(
    db: Session, user_id: int, question: str, k: int = 5, document_id: int | None = None
):
    question_vector = embed_texts([question])[0]
    # cosine_distance comes from pgvector: smaller = more similar.
    distance = Chunk.embedding.cosine_distance(question_vector)

    stmt = (
        select(Chunk, Document.filename, distance.label("distance"))
        .join(Document, Document.id == Chunk.document_id)
        # user_id filter = a user can only ever search their own documents.
        .where(Document.user_id == user_id, Chunk.embedding.is_not(None))
        .order_by(distance)
        .limit(k)
    )
    if document_id is not None:
        stmt = stmt.where(Chunk.document_id == document_id)

    # Each row unpacks as (chunk, filename, distance).
    return db.execute(stmt).all()
