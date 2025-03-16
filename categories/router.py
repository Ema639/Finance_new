from fastapi import APIRouter, HTTPException
from src.categories.schemas import CategoryCreate, CategoryOut
from src.categories.service import (
    create_category,
    get_category_by_id,
    get_categories_by_user,
    update_category,
    delete_category
)

router = APIRouter()


@router.post("/categories", response_model=CategoryOut)
async def create_category_endpoint(category: CategoryCreate):
    try:
        new_category = await create_category(
            name=category.name,
            category_type=category.type,
            user_id=category.user_id,
            description=category.description
        )
        return new_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories/{category_id}", response_model=CategoryOut)
async def get_category_endpoint(category_id: int):
    try:
        category = await get_category_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found.")
        return category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories/user/{user_id}", response_model=list[CategoryOut])
async def get_user_categories(user_id: int):
    try:
        categories = await get_categories_by_user(user_id)
        if not categories:
            raise HTTPException(status_code=404, detail="No categories found for the given user.")
        return categories
    except Exception as e:
        raise HTTPException(status_code=400, detail="Something went wrong while fetching user's categories.")


@router.put("/categories/{category_id}", response_model=CategoryOut)
async def update_category_endpoint(category_id: int, category: CategoryCreate):
    try:
        updated_category = await update_category(
            category_id=category_id,
            name=category.name,
            description=category.description
        )
        if not updated_category:
            raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found.")
        return updated_category
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/categories/{category_id}")
async def delete_category_endpoint(category_id: int):
    try:
        result = await delete_category(category_id)
        if not result:
            raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found.")
        return {"detail": "Category successfully deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
