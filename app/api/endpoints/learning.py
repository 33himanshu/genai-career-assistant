from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.agents.learning import LearningResourceAgent

router = APIRouter(prefix="/learning", tags=["learning"])

class QueryRequest(BaseModel):
    query: str
    
class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = None
    
class TutorialResponse(BaseModel):
    content: str
    file_path: str
    
class ChatResponse(BaseModel):
    content: str
    role: str

@router.post("/tutorial", response_model=TutorialResponse)
async def create_tutorial(request: QueryRequest):
    """Create a tutorial based on the user's query."""
    try:
        agent = LearningResourceAgent()
        result = agent.create_tutorial(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating tutorial: {str(e)}")

@router.post("/query", response_model=ChatResponse)
async def answer_query(request: ChatRequest):
    """Answer a query about Generative AI."""
    try:
        agent = LearningResourceAgent()
        
        # Convert chat history to the format expected by the agent
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
            ]
            
        result = agent.answer_query(request.query, chat_history)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering query: {str(e)}")