from sqlalchemy.future import select
from src.categories.models import Category
from src.database import AsyncSession


# CRUD операции для Категории

async def create_category(name: str, category_type: str, user_id: int, description: str = None) -> Category:
    async with AsyncSession() as session:
        new_category = Category(name=name, type=category_type, user_id=user_id, description=description)
        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)
        return new_category


async def get_category_by_id(category_id: int) -> Category | None:
    async with AsyncSession() as session:
        result = await session.execute(select(Category).filter(Category.id == category_id))
        return result.scalars().first()


async def get_categories_by_user(user_id: int) -> list[Category]:
    async with AsyncSession() as session:
        result = await session.execute(select(Category).filter(Category.user_id == user_id))
        return result.scalars().all()


async def update_category(category_id: int, name: str = None, category_type: str = None,
                          description: str = None) -> Category | None:
    async with AsyncSession() as session:
        result = await session.execute(select(Category).filter(Category.id == category_id))
        category_to_update = result.scalars().first()
        if category_to_update:
            if name:
                category_to_update.name = name
            if category_type:
                category_to_update.type = category_type
            if description:
                category_to_update.description = description
            await session.commit()
        return category_to_update


async def delete_category(category_id: int) -> bool:
    async with AsyncSession() as session:
        result = await session.execute(select(Category).filter(Category.id == category_id))
        category_to_delete = result.scalars().first()
        if category_to_delete:
            await session.delete(category_to_delete)
            await session.commit()
            return True
        return False
