from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    text: Annotated[str, Field(..., min_length=1, description="Текст вопроса")]


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: Annotated[int, Field(..., description="ID вопроса")]
    created_at: Annotated[datetime, Field(..., description="Дата создания")]

    model_config = {"from_attributes": True}


class AnswerBase(BaseModel):
    text: Annotated[str, Field(..., min_length=1, description="Текст ответа")]


class AnswerCreate(AnswerBase):
    user_id: Annotated[UUID, Field(..., description="ID пользователя")]


class AnswerResponse(AnswerBase):
    id: Annotated[int, Field(...)]
    question_id: Annotated[int, Field(...)]
    user_id: Annotated[UUID, Field(...)]
    created_at: Annotated[datetime, Field(...)]

    model_config = {"from_attributes": True}


class QuestionWithAnswers(QuestionResponse):
    answers: Annotated[list[AnswerResponse], Field(description="Список ответов")]
