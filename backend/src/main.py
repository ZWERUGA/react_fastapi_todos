from fastapi import FastAPI

from database.database import create_db_and_tables
from routers.todos import router as todos_router
from routers.users import router as users_router


app = FastAPI()

app.include_router(todos_router)
app.include_router(users_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
