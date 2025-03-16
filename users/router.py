from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from src.users.schemas import UserCreate, UserOut
from src.users.service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)

router = APIRouter()


@router.post("/users", response_model=UserOut)
async def create_user_endpoint(user: UserCreate):
    try:
        new_user = await create_user(name=user.name, email=str(user.email), password_hash=user.password)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users", response_model=list[UserOut])
async def list_users():
    try:
        users = await get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int):
    try:
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: int, user_update: UserCreate):
    try:
        updated_user = await update_user(
            user_id=user_id,
            name=user_update.name,
            email=str(user_update.email),
            password_hash=user_update.password
        )
        if not updated_user:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{user_id}")
async def delete_user_endpoint(user_id: int):
    try:
        result = await delete_user(user_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
        return {"detail": "User successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Finance App</h1>"
