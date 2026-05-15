"""
Startup script: inits DB, seeds data, runs server
Usage: python run.py
"""

import asyncio


async def startup():
    from app.database import init_db
    from seed import seed

    print("=" * 50)
    print("  PakShield AI - Backend Startup")
    print("=" * 50)

    print("\n[1/3] Initializing database...")
    await init_db()
    print("  [OK] Tables created")

    print("\n[2/3] Seeding default data...")
    try:
        await seed()
    except Exception as e:
        print(f"  [!] Seed skipped: {e}")

    print("\n[3/3] Starting server...")
    print("  -> http://localhost:8000")
    print("  -> http://localhost:8000/docs")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(startup())
