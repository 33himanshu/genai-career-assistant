from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

from app.agents.interview import InterviewAgent

router = APIRouter(prefix="/interview", tags=["interview"])

class QueryRequest(BaseModel):
    query: str
    
class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[ChatMessage]] = None
    
class InterviewResponse(BaseModel):
    content: str
    file_path: str
    
class ChatResponse(BaseModel):
    content: str
    role: str

@router.post("/questions", response_model=InterviewResponse)
async def generate_interview_questions(request: QueryRequest):
    """Generate interview questions based on the user's query."""
    try:
        agent = InterviewAgent()
        result = agent.generate_interview_questions(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview questions: {str(e)}")

@router.post("/mock", response_model=ChatResponse)
async def conduct_mock_interview(request: ChatRequest):
    """Conduct a mock interview session."""
    try:
        agent = InterviewAgent()
        
        # Convert chat history to the format expected by the agent
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
            ]
            
        result = agent.conduct_mock_interview(request.query, chat_history)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error conducting mock interview: {str(e)}")
