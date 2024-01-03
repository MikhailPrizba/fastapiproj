from datetime import datetime

from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    id: int
    title: str
    author_id: int
    assignee_id: int

    class Config:
        from_attributes = True


class TaskSchemaAdd(BaseModel):
    title: str
    assignee_id: int
