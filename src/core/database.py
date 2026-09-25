from src.core.config import settings
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async def get_checkpointer():
    """Provide an asynchronous PostgreSQL checkpointer for graph persistence."""
    return AsyncPostgresSaver.from_conn_string(settings.DB_URI)