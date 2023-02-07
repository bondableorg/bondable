from core.db import AsyncDBSession


async def get_db_session():
    async with AsyncDBSession() as session:
        yield session
        await session.commit()
