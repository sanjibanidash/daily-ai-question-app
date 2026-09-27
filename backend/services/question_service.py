from openai import OpenAI

from backend.config.settings import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_question(difficulty: str) -> str:

    prompt = f"""
Generate ONE interview-style question for someone learning
Data Science and AI.

Difficulty: {difficulty}

Choose the topic yourself.

For Easy questions, focus on:
- Python
- SQL
- Statistics
- Machine Learning fundamentals

For Medium questions, focus on:
- Feature Engineering
- Model Evaluation
- Deep Learning
- NLP
- Time Series

For Hard questions, focus on:
- MLOps
- ML System Design
- LLMs
- RAG
- AI Agents
- AI Engineering
- Generative AI

Rules:
- Generate exactly ONE question.
- Test understanding, not memorization.
- Keep the question clear and concise.
- Do not provide the answer.
- Do not mention the difficulty.
- Do not number the question.
- Return only the question.
"""

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text.strip()