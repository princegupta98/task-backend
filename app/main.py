from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, projects, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Task Management App is running"}
