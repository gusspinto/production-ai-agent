from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from src.agent.graph import workflow
from src.api.routes import router as api_router
from src.core.database import DB_URI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle, initializing the database checkpointer and graph."""
    async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
        await checkpointer.setup()
        app.state.graph = workflow.compile(checkpointer=checkpointer)
        yield

app = FastAPI(title="Production AI Agent API with LangGraph", lifespan=lifespan)

app.include_router(api_router)