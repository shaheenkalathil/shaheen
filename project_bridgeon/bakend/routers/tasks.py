from fastapi import APIRouter, HTTPException
from bakend.models import TaskCreate, TaskUpdate
from database import get_connection

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/{username}")
def create_task(username: str, task: TaskCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks(
        username,
        title,
        description,
        priority,
        due_date
    )
    VALUES(?,?,?,?,?)
    """, (
        username,
        task.title,
        task.description,
        task.priority,
        task.due_date
    ))

    conn.commit()
    conn.close()

    return {"message": "Task created"}

@router.get("/{username}")
def get_tasks(username: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE username=?",
        (username,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

@router.delete("/{task_id}")
def delete_task(task_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    conn.close()

    return {
        "message": "Task deleted"
    }

@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks
    SET
    title=?,
    description=?,
    priority=?,
    due_date=?,
    completed=?
    WHERE id=?
    """,
    (
        task.title,
        task.description,
        task.priority,
        task.due_date,
        int(task.completed),
        task_id
    ))

    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    conn.close()

    return {"message": "Task updated"}

@router.get("/")
def search_tasks(completed: bool):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM tasks
        WHERE completed=?
        """,
        (int(completed),)
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]