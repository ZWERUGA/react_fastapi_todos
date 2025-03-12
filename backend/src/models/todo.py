from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    text: str
    is_completed: bool = Field(default=False)


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
