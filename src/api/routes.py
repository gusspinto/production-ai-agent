from fastapi import APIRouter, Request
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

router = APIRouter()

class MessageRequest(BaseModel):
    question: str
    user_id: str = "default_user"

@router.post("/chat")
async def chat_with_agent(request: Request, body: MessageRequest):
    """Process incoming chat messages and execute the LangGraph workflow."""
    initial_state = {"messages": [HumanMessage(content=body.question)]}
    config = {"configurable": {"thread_id": body.user_id}}
    
    graph = request.app.state.graph
    final_state = await graph.ainvoke(initial_state, config)
    final_message = final_state["messages"][-1]

    return {
        "response_agent": final_message.content
    }