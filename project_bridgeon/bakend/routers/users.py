from fastapi import APIRouter, HTTPException
from models import UserCreate, UserLogin
from database import get_connection
from schemas import UserCreate, UserLogin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(user: UserCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (user.username,)
    )

    if cursor.fetchone():
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (
            user.username,
            user.email,
            user.password
        )
    )

    conn.commit()
    conn.close()

    return {"message": "Registration successful"}


@router.post("/login")
def login(user: UserLogin):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (
            user.username,
            user.password
        )
    )

    found = cursor.fetchone()

    conn.close()

    if not found:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "message": "Login successful",
        "username": user.username
    }