from fastapi import FastAPI

from .routers import answers_router, qa_router, questions_router

app = FastAPI(version="0.1.0", description="QA API", title="QA API")


app.include_router(questions_router)
app.include_router(qa_router)
app.include_router(answers_router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to QA API"}
