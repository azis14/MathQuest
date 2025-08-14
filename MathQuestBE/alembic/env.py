import sys, asyncio
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.core.config import settings

target_metadata = Base.metadata

DB_URL = settings.database_url_sync
print("Using sync database URL:", DB_URL)

def raise_offline():
    raise RuntimeError("Offline migrations are disabled for this project.")

def do_configure(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    engine = create_async_engine(DB_URL, future=True, pool_pre_ping=True)
    async with engine.connect() as conn:
        await conn.run_sync(do_configure)


if context.is_offline_mode():
    raise_offline()
else:
    asyncio.run(run_migrations_online())