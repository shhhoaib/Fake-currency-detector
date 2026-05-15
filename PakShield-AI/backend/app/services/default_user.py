from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.services.auth_service import hash_password

DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"


async def get_default_user(db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == DEFAULT_USER_ID))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            id=DEFAULT_USER_ID,
            email="system@pakshield.ai",
            username="system",
            hashed_password=hash_password("system"),
            is_active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user
