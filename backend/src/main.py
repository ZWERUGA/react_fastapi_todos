from typing import Annotated
from fastapi import Depends, FastAPI

from services.users import get_current_user
from schemas.users import User, UserPublic
from database.database import create_db_and_tables
from routers.todos import router as todos_router
from routers.users import router as users_router


app = FastAPI()

app.include_router(todos_router)
app.include_router(users_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/users/me/", response_model=UserPublic)
async def read_users_me(
    current_user: Annotated[UserPublic, Depends(get_current_user)],
):
    return current_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
