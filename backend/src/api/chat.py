from fastapi import APIRouter, HTTPException
from google.genai import errors as genai_errors

from api.deps import CurrentUser, DBSession
from schemas.chat import AskRequest, AskResponse, Citation
from services.answering import answer_question
from services.retrieval import search_chunks

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=AskResponse)
def ask(data: AskRequest, user: CurrentUser, db: DBSession):
    hits = search_chunks(db, user.id, data.question, document_id=data.document_id)
    if not hits:
        return AskResponse(
            answer="I couldn't find any uploaded documents to search. Upload a PDF first.",
            citations=[],
        )

    try:
        answer = answer_question(data.question, hits)
    except genai_errors.APIError as e:
        print("Gemini API error:", repr(e))
        if e.code == 503:
            raise HTTPException(
                status_code=503, detail="The AI service is busy. Try again in a minute."
            )
        # 429 = free-tier rate limit hit.
        if e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="Rate limit reached. Wait a minute and try again.",
            )
        raise HTTPException(status_code=502, detail="The AI service failed. Try again.")

    citations = [
        Citation(
            index=i,
            document_id=chunk.document_id,
            filename=filename,
            page=chunk.page_no,
            snippet=chunk.text[:300],
        )
        for i, (chunk, filename, _) in enumerate(hits, start=1)
    ]
    return AskResponse(answer=answer, citations=citations)
