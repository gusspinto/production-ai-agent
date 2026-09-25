from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()

import sqlite3
import asyncio
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
from tools import calculate_imc

DB_URI = "postgresql://postgres:postgres@localhost:5432/ai_agent_db"

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
        await checkpointer.setup()

        app.state.graph = workflow.compile(checkpointer=checkpointer)
        yield

# create a FastAPI app
app = FastAPI(title="Production AI Agent API with LangGraph", lifespan=lifespan)

llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)
# bind the tools to the LLM
tools = [calculate_imc]
llm_with_tools = llm.bind_tools(tools)

# define the workflow for the agent using LangGraph
def call_model(state: MessagesState):
    # get the current messages from the state
    messages = state["messages"]
    # invoke the LLM with the current messages
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
tool_node = ToolNode(tools=tools)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    }
)

workflow.add_edge("tools", "agent")

# if the graoh was still be complied here it would be static and not be able to save the state of the conversation. So we need to compile it after we have a checkpointer.

#conn = sqlite3.connect("chatbot.db", check_same_thread=False)
#memory = SqliteSaver(conn)
#app_graph = workflow.compile(checkpointer=memory)

class MessageRequest(BaseModel):
    question: str
    user_id: str = "default_user"

@app.post("/chat")
async def chat_with_agent(request: MessageRequest):
    initial_state = {"messages": [HumanMessage(content=request.question)]}
    config = {"configurable": {"thread_id": request.user_id}}
    # with Postgres its totaly assynchronous so we can use ainvoke instead of invoke
    final_state = await app.state.graph.ainvoke(initial_state, config)
    final_message = final_state["messages"][-1]

    return {
        "response_agent": final_message.content
    }