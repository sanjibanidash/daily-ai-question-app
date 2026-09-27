from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.question_service import generate_question


router = APIRouter()


class QuestionRequest(BaseModel):
    difficulty: str


@router.post("/question")
def create_question(request: QuestionRequest):

    question = generate_question(
        difficulty=request.difficulty
    )

    return {
        "question": question,
        "difficulty": request.difficulty,
    }