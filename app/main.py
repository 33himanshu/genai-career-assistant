from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.api.router import router
from app.workflows.graph import create_workflow

app = FastAPI(
    title="GenAI Career Assistant API",
    description="API for a career assistant specializing in Generative AI careers",
    version="1.0.0"
)

# Include API routers
app.include_router(router, prefix="/api")

class QueryRequest(BaseModel):
    query: str

class WorkflowResponse(BaseModel):
    category: str
    response: str

# Create the workflow graph
workflow = create_workflow()

@app.post("/workflow", response_model=Dict[str, Any])
async def run_workflow(request: QueryRequest):
    """Run the complete workflow based on the user's query."""
    try:
        result = workflow.invoke({"query": request.query})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running workflow: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "GenAI Career Assistant API is running"}