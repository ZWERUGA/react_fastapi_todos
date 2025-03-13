from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    text: str


class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    is_completed: bool = Field(default=False)


class TodoPublic(TodoBase):
    id: int
    is_completed: bool


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    text: str | None = None
    is_completed: bool | None = None
