from fastapi import FastAPI

from backend.api.routes import router


app = FastAPI(
    title="Daily AI Question App",
    description="Generates beginner-friendly Data Science and AI interview questions.",
    version="1.0.0",
)


app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "Daily AI Question API is running.",
    }