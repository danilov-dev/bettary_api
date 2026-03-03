from sqlalchemy.ext.asyncio import (AsyncSession,
                                    create_async_engine,
                                    async_sessionmaker)

from sqlalchemy.orm import declarative_base

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=True,
    connect_args={'check_same_thread': False}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session