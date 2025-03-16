from fastapi import FastAPI
import uvicorn
from src.database import engine, Base
from contextlib import asynccontextmanager
from src.users.router import router as users_router
from src.categories.router import router as categories_router
from src.transactions.router import router as transactions_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Finance App", lifespan=lifespan)

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(transactions_router, prefix="/transactions", tags=["Transactions"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
