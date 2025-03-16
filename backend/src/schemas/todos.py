from pydantic import BaseModel, ConfigDict


class TodoBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Todo(TodoBase):
    id: int
    text: str
    is_completed: bool


class TodoCreate(TodoBase):
    text: str


class TodoUpdate(TodoBase):
    text: str | None = None
    is_completed: bool | None = None
