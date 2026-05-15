"""
Seed database with test user
Run: python seed.py
"""

import asyncio
from app.database import init_db, async_session
from app.models.user import User
from app.services.auth_service import hash_password


async def seed():
    await init_db()
    async with async_session() as db:
        from sqlalchemy import select
        existing = await db.execute(select(User).where(User.username == "admin"))
        if existing.scalar_one_or_none():
            print("Admin user already exists, skipping seed.")
            return

        user = User(
            email="admin@pakshield.ai",
            username="admin",
            hashed_password=hash_password("admin123"),
        )
        db.add(user)
        await db.commit()
        print("[OK] Seed complete: admin / admin123")


if __name__ == "__main__":
    asyncio.run(seed())
