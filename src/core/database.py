import os
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

DB_URI = os.getenv("DB_URI", "postgresql://postgres:postgres@localhost:5432/ai_agent_db")

async def get_checkpointer():
    """Provide an asynchronous PostgreSQL checkpointer for graph persistence."""
    return AsyncPostgresSaver.from_conn_string(DB_URI)