from fastapi import APIRouter
from app.api.endpoints import learning, interview, resume, job

router = APIRouter()

router.include_router(learning.router)
router.include_router(interview.router)
router.include_router(resume.router)
router.include_router(job.router)