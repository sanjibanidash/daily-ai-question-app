from fastapi import APIRouter
from pydantic import BaseModel
from typing import Literal, Optional

from backend.services.question_service import generate_question
from backend.database import get_connection


router = APIRouter()


# -----------------------------
# Question API
# -----------------------------

class QuestionRequest(BaseModel):
    difficulty: str
    topic: Optional[
        Literal[
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Deep Learning",
            "Generative AI",
            "NLP",
            "MLOps",
        ]
    ] = None



@router.post("/question")
def create_question(request: QuestionRequest):
    question = generate_question(
        difficulty=request.difficulty,
        topic=request.topic,
    )

    # Log the generated question without breaking question generation.
    try:
        connection = get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO public.generated_questions
                        (question, difficulty, topic)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        question,
                        request.difficulty,
                        request.topic or "Automatic",
                    ),
                )
            connection.commit()
        finally:
            connection.close()

    except Exception as exc:
        print(f"Question logging failed: {exc}")

    return {
        "question": question,
        "difficulty": request.difficulty,
        "topic": request.topic or "Automatic",
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