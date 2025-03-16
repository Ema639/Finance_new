from sqlalchemy.future import select
from src.users.models import User
from src.database import AsyncSession


# CRUD операции для Пользователя

async def create_user(name: str, email: str
, password_hash: str) -> User:
    async with AsyncSession() as session:
        new_user = User(name=name, email=email, password_hash=password_hash)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def get_user_by_id(user_id: int) -> User | None:
    async with AsyncSession() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()


async def get_all_users() -> list[User]:
    async with AsyncSession() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def update_user(user_id: int, name: str = None, email: str = None, password_hash: str = None) -> User | None:
    async with AsyncSession() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
        user_to_update = result.scalars().first()
        if user_to_update:
            if name:
                user_to_update.name = name
            if email:
                user_to_update.email = email
            if password_hash:
                user_to_update.password_hash = password_hash
            await session.commit()
        return user_to_update


async def delete_user(user_id: int) -> bool:
    async with AsyncSession() as session:
        result = await session.execute(select(User).filter(User.id == user_id))
        user_to_delete = result.scalars().first()
        if user_to_delete:
            await session.delete(user_to_delete)
            await session.commit()
            return True
        return False
