from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        connect_args = {}
        if settings.database_url.startswith("sqlite"):
            connect_args = {"check_same_thread": False}
        _engine = create_async_engine(
            settings.database_url,
            echo=False,
            connect_args=connect_args,
        )
    return _engine


async_session = async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with get_engine().begin() as conn:
        def _migrate(conn):
            import sqlalchemy as sa
            inspector = sa.inspect(conn)
            columns = [c["name"] for c in inspector.get_columns("scan_records")]
            for col in ["feature_scores_json", "security_json", "reasons_json"]:
                if col not in columns:
                    conn.execute(sa.text(f"ALTER TABLE scan_records ADD COLUMN {col} TEXT"))
        await conn.run_sync(_migrate)
