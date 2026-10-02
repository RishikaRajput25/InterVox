from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag.rag_service import rag_service


router = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


class QuestionRequest(BaseModel):
    question: str
    document_id: str


class QuestionResponse(BaseModel):
    answer: str
    sources: list[dict]


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty",
        )

    if not request.document_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Document ID cannot be empty",
        )

    try:
        result = rag_service.ask(
            query=request.question,
            document_id=request.document_id,
        )

        return QuestionResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {error}",
        )