from fastapi import APIRouter, HTTPException, UploadFile, status
from sqlalchemy import select

from api.deps import CurrentUser, DBSession
from models.chunk import Chunk
from models.document import Document
from schemas.document import DocumentRead
from services.chunking import chunk_text
from services.embeddings import embed_texts
from services.pdf import extract_pages

router = APIRouter(prefix="/documents", tags=["documents"])

# 20M Max Upload Size
MAX_UPLOAD_SIZE = 20 * 1024 * 1024


@router.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def upload_document(file: UploadFile, user: CurrentUser, db: DBSession):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="only PDF files are supported.",
        )
    if file.size is not None and file.size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="PDF File Exceeds Max Upload Size Limit!",
        )

    try:
        pages = extract_pages(file.file)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could Not Read The PDF."
        )

    document = Document(user_id=user.id, filename=file.filename)
    db.add(document)
    db.flush()

    chunks = []
    #     index = 0
    #
    #     for pageN, text in pages:
    #         for piece in chunk_text(text):
    #             chunks.append(
    #                 Chunk(
    #                     document_id=document.id,
    #                     page_no=pageN,
    #                     chunk_index=index,
    #                     text=piece,
    #                 )
    #             )
    #             index += 1

    # Collect (page, text) pairs first, then embed them all in one batch.
    pieces = []
    for page_number, text in pages:
        for piece in chunk_text(text):
            pieces.append((page_number, piece))

    vectors = embed_texts([piece for _, piece in pieces])

    chunks = [
        Chunk(
            document_id=document.id,
            page_no=page_number,
            chunk_index=index,
            text=piece,
            embedding=vector,
        )
        for index, ((page_number, piece), vector) in enumerate(zip(pieces, vectors))
    ]

    db.add_all(chunks)
    db.commit()
    db.refresh(document)

    return document


@router.get("/", response_model=list[DocumentRead])
def list_documents(user: CurrentUser, db: DBSession):
    return db.scalars(
        select(Document)
        .where(Document.user_id == user.id)
        .order_by(Document.created_at.desc())
    ).all()


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(documentID: int, user: CurrentUser, db: DBSession):
    document = db.scalar(
        select(Document).where(Document.id == documentID, Document.user_id == user.id)
    )

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document Not Found!"
        )

    db.delete(document)
    db.commit()
