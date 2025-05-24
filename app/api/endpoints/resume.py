from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.resume import ResumeMaker

router = APIRouter(prefix="/resume", tags=["resume"])

class QueryRequest(BaseModel):
    query: str
    
class ResumeResponse(BaseModel):
    content: str
    file_path: str

@router.post("/create", response_model=ResumeResponse)
async def create_resume(request: QueryRequest):
    """Create a resume based on the user's query."""
    try:
        agent = ResumeMaker()
        result = agent.create_resume(request.query)
        return result
    except Exception as e:
        # Log the error
        print(f"Error creating resume: {str(e)}")
        
        # Create a fallback response
        agent = ResumeMaker()
        agent.use_fallback = True
        result = agent.create_resume(request.query)
        return result
