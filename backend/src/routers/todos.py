from typing import Annotated
from fastapi import APIRouter, Depends

from services.users import get_current_user
from schemas.users import UserPublic
from schemas.todos import Todo, TodoCreate, TodoUpdate
from database.database import SessionDep
import services.todos as service


router = APIRouter(prefix="/todos")


@router.get("/", response_model=list[Todo])
def get_todos(
    session: SessionDep, user: Annotated[UserPublic, Depends(get_current_user)]
):
    """
    Получение всех задач из БД.
    """
    return service.get_todos(session=session, user=user)


@router.get("/{todo_id}", response_model=Todo)
def get_todo(
    todo_id: int,
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_user)],
):
    """
    Получение задачи из БД по ID.
    """
    return service.get_todo(todo_id=todo_id, user=user, session=session)


@router.post("/", response_model=Todo)
def create_todo(
    todo: TodoCreate,
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_user)],
):
    """
    Создание задачи и добавление в БД.
    """
    return service.create_todo(todo=todo, user=user, session=session)


@router.patch("/{todo_id}", response_model=Todo)
def update_todo(
    todo_id: int,
    todo: TodoUpdate,
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_user)],
):
    """
    Обновление задачи в БД.
    """
    return service.update_todo(todo_id=todo_id, todo=todo, user=user, session=session)


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    session: SessionDep,
    user: Annotated[UserPublic, Depends(get_current_user)],
):
    """
    Удаление задачи из БД.
    """
    return service.delete_todo(todo_id=todo_id, user=user, session=session)
