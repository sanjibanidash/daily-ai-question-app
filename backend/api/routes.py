from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.question_service import generate_question
from backend.database import get_connection


router = APIRouter()


# -----------------------------
# Question API
# -----------------------------

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


# -----------------------------
# Login API
# -----------------------------

class LoginRequest(BaseModel):
    name: str
    email: str


@router.post("/login")
def login_user(request: LoginRequest):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, last_login_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP)

        ON CONFLICT (email)
        DO UPDATE SET
            name = EXCLUDED.name,
            last_login_at = CURRENT_TIMESTAMP

        RETURNING id, name, email, last_login_at;
        """,
        (request.name, request.email),
    )

    user = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Login recorded successfully",
        "user": {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "last_login_at": user[3],
        },
    }