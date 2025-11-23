from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.db_depends import get_db
from app.database.models import Question
from app.schemas import QuestionCreate, QuestionResponse, QuestionWithAnswers

questions_router = APIRouter(prefix="/questions", tags=["Questions"])


@questions_router.get("/", response_model=list[QuestionResponse])
async def get_all_questions(db: AsyncSession = Depends(get_db)):
    stmt = select(Question).options(selectinload(Question.answers))
    result = await db.execute(stmt)
    questions = result.scalars().all()
    return questions


@questions_router.post("/", response_model=QuestionResponse, status_code=201)
async def create_question(question: QuestionCreate, db: AsyncSession = Depends(get_db)):
    new_question = Question(**question.model_dump())
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return new_question


@questions_router.get("/{id}", response_model=QuestionWithAnswers)
async def get_question(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Question).options(selectinload(Question.answers)).where(Question.id == id)
    result = await db.execute(stmt)
    question = result.scalars().one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@questions_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(id: int, db: AsyncSession = Depends(get_db)):
    question_to_delete = await db.get(Question, id)
    if not question_to_delete:
        raise HTTPException(status_code=404, detail="Question not found")
    await db.delete(question_to_delete)
    await db.commit()
    return
