from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents.job import JobSearch

router = APIRouter(prefix="/job", tags=["job"])

class QueryRequest(BaseModel):
    query: str
    
class JobResponse(BaseModel):
    content: str
    file_path: str

@router.post("/search", response_model=JobResponse)
async def search_jobs(request: QueryRequest):
    """Search for jobs based on the user's query."""
    try:
        agent = JobSearch()
        result = agent.find_jobs(request.query)
        return result
    except Exception as e:
        # Log the error
        print(f"Error in job search: {str(e)}")
        
        # Create a fallback response
        agent = JobSearch()
        agent.use_fallback = True
        result = agent.find_jobs(request.query)
        return result



