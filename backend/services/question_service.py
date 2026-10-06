from openai import OpenAI
from backend.config.settings import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    default_headers={
        "Accept-Encoding": "identity",
    },
)


def generate_question(difficulty: str) -> str:

    prompt = f"""
You are an expert Data Science and AI technical interviewer.

Your job is to generate ONE high-quality interview question for a
learner preparing for Data Science and AI interviews.

Difficulty level: {difficulty}

IMPORTANT:
Difficulty must be determined by the amount of reasoning required,
NOT simply by the topic.

--------------------------------------------------
EASY
--------------------------------------------------

- Test ONE fundamental concept.
- Require simple understanding or basic reasoning.
- Suitable for a beginner.
- Focus on one concept only.
- Prefer topics such as:
  Python, SQL, statistics, data preprocessing,
  machine learning fundamentals, and basic data concepts.

Example styles:

"What is overfitting in machine learning?"

"What is the difference between a list and a tuple in Python?"

"What does a primary key do in a database?"

--------------------------------------------------
MEDIUM
--------------------------------------------------

- Test application of a concept.
- Use a small practical situation or model behavior.
- Require the candidate to interpret, choose, or reason about ONE thing.
- Suitable for someone with basic Data Science knowledge.
- Prefer topics such as:
  feature engineering, model evaluation, cross-validation,
  class imbalance, time series, NLP, and model selection.

Example styles:

"A classification model has high accuracy but performs poorly on the
minority class. Which evaluation metric would you examine?"

"A machine learning model performs very well on training data but poorly
on unseen data. What problem is most likely occurring?"

--------------------------------------------------
HARD
--------------------------------------------------

- Test ONE deep technical reasoning skill.
- Use a realistic Data Science, AI, or production scenario.
- Focus on exactly ONE of these areas:
  debugging,
  model selection,
  experiment design,
  production failure analysis,
  monitoring,
  system design,
  or technical trade-offs.
- Do NOT combine multiple areas in one question.
- Do NOT ask the candidate to design an entire end-to-end system.
- The question should be answerable in approximately 2-5 minutes.
- Prefer a focused scenario that requires thoughtful reasoning.

Example styles:

"Your model's validation performance is good, but its production
performance drops sharply. What would you investigate first?"

"You have two models with similar accuracy, but one is much slower during
inference. Which would you choose for a real-time application?"

"A deployed model's prediction distribution suddenly changes.
What could cause this?"

--------------------------------------------------
STRICT OUTPUT RULES
--------------------------------------------------

1. Generate exactly ONE interview question.
2. Ask exactly ONE main task.
3. The question must be answerable with ONE primary response.
4. Do not combine multiple tasks.
5. Avoid questions that require several separate deliverables.
6. Avoid "and why", "and explain", or "and provide an example" when
   they create a second task.
7. Do not ask for architecture + metrics + monitoring + deployment
   in the same question.
8. For Hard questions, test ONE deep skill only.
9. Do not provide the answer.
10. Do not provide hints.
11. Do not mention the difficulty level.
12. Do not number the question.
13. Do not write "Question:" before it.
14. Keep the question clear and concise.
15. Avoid trivia and memorization-only questions.
16. Make the question useful for a real Data Science or AI interview.
17. Avoid overly broad case studies.
18. Return ONLY the question text.

Generate the question now.
"""

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=prompt,
    )

    return response.output_text.strip()