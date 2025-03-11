from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
