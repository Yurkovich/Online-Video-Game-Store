from fastapi import APIRouter, HTTPException
from schemas.auth_schema import UserRegistration
import sqlite3

router = APIRouter()

@router.post("/api/register")
async def register_user(user_data: UserRegistration):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (user_data.email, user_data.password)
        )
        conn.commit()
        return {"message": "User registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")
    finally:
        conn.close()