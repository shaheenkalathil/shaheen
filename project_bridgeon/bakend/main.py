from fastapi import FastAPI
from database import init_db
from bakend.routers.tasks import router as task_router
from routers.users import router as user_router

app = FastAPI(
    title="Task Manager API"
)

init_db()
 
app.include_router(user_router)
app.include_router(task_router)