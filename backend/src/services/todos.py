from fastapi import HTTPException
from sqlalchemy import select, update

from schemas.todos import Todo, TodoCreate, TodoUpdate
from models.todos import Todo as TodoORM
from database.database import SessionDep


def get_todos(session: SessionDep):
    """
    Получение всех задач из БД.
    """
    todos = session.execute(select(TodoORM)).scalars().all()
    return [Todo(id=t.id, text=t.text, is_completed=t.is_completed) for t in todos]


def get_todo(todo_id: int, session: SessionDep):
    """
    Получение задачи из БД по ID.
    """
    todo = session.get(TodoORM, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found...")
    return todo


def create_todo(todo: TodoCreate, session: SessionDep):
    """
    Создание задачи и добавление в БД.
    """
    new_todo = TodoORM(**todo.model_dump())
    session.add(new_todo)
    session.commit()
    return new_todo


def update_todo(todo_id: int, todo: TodoUpdate, session: SessionDep):
    """
    Обновление задачи в БД.
    """
    db_todo = session.get(TodoORM, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found...")

    todo_data = todo.model_dump(exclude_unset=True)
    session.execute(update(TodoORM).where(TodoORM.id == todo_id).values(todo_data))
    session.commit()
    return db_todo


def delete_todo(todo_id: int, session: SessionDep):
    """
    Удаление задачи из БД.
    """
    db_todo = session.get(TodoORM, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found...")

    session.delete(db_todo)
    session.commit()
    return get_todos(session=session)
