from fastapi import APIRouter, HTTPException
from sqlmodel import select

from models.todos import Todo, TodoPublic, TodoCreate, TodoUpdate
from database.database import SessionDep


router = APIRouter(prefix="/todos")


@router.get("/", response_model=list[TodoPublic])
def get_todos(session: SessionDep):
    """
    Получение всех задач из БД.
    """
    todos = session.exec(select(Todo)).all()
    return todos


@router.get("/{todo_id}", response_model=TodoPublic)
def get_todo(todo_id: int, session: SessionDep):
    """
    Получение задачи из БД по ID.
    """
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found...")
    return todo


@router.post("/", response_model=TodoPublic)
def create_todo(todo: TodoCreate, session: SessionDep):
    """
    Создание задачи и добавление в БД.
    """
    db_todo = Todo.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.patch("/{todo_id}", response_model=TodoPublic)
def update_todo(todo_id: int, todo: TodoUpdate, session: SessionDep):
    """
    Обновление задачи в БД.
    """
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found...")

    todo_data = todo.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep):
    """
    Удаление задачи из БД.
    """
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found...")

    session.delete(db_todo)
    session.commit()
    return {"message": "Todo deleted"}
