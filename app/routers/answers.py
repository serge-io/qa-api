from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_depends import get_db
from app.database.models import Answer, Question
from app.schemas import AnswerCreate, AnswerResponse

answers_router = APIRouter(prefix="/answers", tags=["Answers"])
qa_router = APIRouter(prefix="/questions", tags=["Answers"])


@qa_router.post(
    "/{question_id}/answers",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(question_id: int, answer: AnswerCreate, db: AsyncSession = Depends(get_db)):
    question = await db.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    new_answer = Answer(question_id=question_id, **answer.model_dump())

    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    return new_answer


@answers_router.get("/{answer_id}", response_model=AnswerResponse)
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    answer = await db.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@answers_router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    answer_to_delete = await db.get(Answer, answer_id)
    if not answer_to_delete:
        raise HTTPException(status_code=404, detail="Answer not found")
    await db.delete(answer_to_delete)
    await db.commit()
    return
