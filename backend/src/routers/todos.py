from fastapi import APIRouter, HTTPException
from sqlmodel import select

from models.todos import Todo, TodoPublic, TodoCreate, TodoUpdate
from database.database import SessionDep
import services.todos as service


router = APIRouter(prefix="/todos")


@router.get("/", response_model=list[TodoPublic])
def get_todos(session: SessionDep):
    """
    Получение всех задач из БД.
    """
    return service.get_todos(session=session)


@router.get("/{todo_id}", response_model=TodoPublic)
def get_todo(todo_id: int, session: SessionDep):
    """
    Получение задачи из БД по ID.
    """
    return service.get_todo(todo_id=todo_id, session=session)


@router.post("/", response_model=TodoPublic)
def create_todo(todo: TodoCreate, session: SessionDep):
    """
    Создание задачи и добавление в БД.
    """
    return service.create_todo(todo=todo, session=session)


@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(todo_id: int, todo: TodoUpdate, session: SessionDep):
    """
    Обновление задачи в БД.
    """
    return service.update_todo(todo_id=todo_id, todo=todo, session=session)


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep):
    """
    Удаление задачи из БД.
    """
    return service.delete_todo(todo_id=todo_id, session=session)
