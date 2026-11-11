from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    # Optional: limit the search to one document.
    document_id: int | None = None


class Citation(BaseModel):
    index: int  # matches the [n] markers in the answer text
    document_id: int
    filename: str
    page: int
    snippet: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
