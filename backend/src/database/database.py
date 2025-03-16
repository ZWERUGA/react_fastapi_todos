from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from models.todos import Todo
from models.users import User


sqlite_file_name = "todos.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    Todo.metadata.create_all(engine)
    User.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
