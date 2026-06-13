from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    due_date: str
    completed: bool