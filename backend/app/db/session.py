from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Union
from app.core.config import DATABASE_URL, DATABASE_MODE

if DATABASE_MODE == "postgres":
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
else:
    engine = None
    async_session = None

async def get_db_session() -> AsyncGenerator[Union[AsyncSession, None], None]:
    if DATABASE_MODE == "postgres":
        async with async_session() as session:
            yield session
    else:
        yield None