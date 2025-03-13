from fastapi import FastAPI

from database.database import create_db_and_tables
from routers.todos import router


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
