from fastapi import Depends
from app.db.session import get_session, AsyncSession

async def get_db(session: AsyncSession = Depends(get_session)):
    async with session.begin():
        yield session
