import pytest
from unittest.mock import patch, MagicMock

from app.agents.learning import LearningResourceAgent
from app.agents.interview import InterviewAgent
from app.agents.resume import ResumeMaker
from app.agents.job import JobSearch

def test_learning_resource_agent_create_tutorial(mock_google_llm, mock_duckduckgo, mock_file_utils, api_key_env):
    """Test the LearningResourceAgent's create_tutorial method."""
    agent = LearningResourceAgent()
    result = agent.create_tutorial("How to use Generative AI for text generation")
    
    assert "content" in result
    assert "file_path" in result
    assert result["file_path"] == "mocked/file/path.md"

def test_learning_resource_agent_answer_query(mock_google_llm, api_key_env):
    """Test the LearningResourceAgent's answer_query method."""
    agent = LearningResourceAgent()
    result = agent.answer_query("What is generative AI?")
    
    assert "content" in result
    assert "role" in result
    assert result["role"] == "assistant"

def test_interview_agent_generate_questions(mock_google_llm, mock_duckduckgo, mock_file_utils, api_key_env):
    """Test the InterviewAgent's generate_interview_questions method."""
    agent = InterviewAgent()
    result = agent.generate_interview_questions("What are common interview questions for AI engineers?")
    
    assert "content" in result
    assert "file_path" in result
    assert result["file_path"] == "mocked/file/path.md"

def test_interview_agent_conduct_mock_interview(mock_google_llm, api_key_env):
    """Test the InterviewAgent's conduct_mock_interview method."""
    agent = InterviewAgent()
    
    # Test initial message (no chat history)
    result = agent.conduct_mock_interview("I'm ready for the interview")
    assert "content" in result
    assert "role" in result
    assert result["role"] == "assistant"
    
    # Test with chat history
    chat_history = [
        {"role": "user", "content": "I have experience with PyTorch and TensorFlow"},
        {"role": "assistant", "content": "Great! Can you tell me about a project where you used these frameworks?"}
    ]
    result = agent.conduct_mock_interview("I built a generative model for text completion", chat_history)
    assert "content" in result
    assert "role" in result

def test_resume_maker_create_resume(mock_google_llm, mock_duckduckgo, mock_file_utils, api_key_env):
    """Test the ResumeMaker's create_resume method."""
    agent = ResumeMaker()
    result = agent.create_resume("Create a resume for an AI engineer with 3 years of experience")
    
    assert "content" in result
    assert "file_path" in result
    assert result["file_path"] == "mocked/file/path.md"

def test_job_search_find_jobs(mock_google_llm, mock_duckduckgo, mock_file_utils, api_key_env):
    """Test the JobSearch's find_jobs method."""
    agent = JobSearch()
    result = agent.find_jobs("Find AI engineer jobs in San Francisco")
    
    assert "content" in result
    assert "file_path" in result
    assert result["file_path"] == "mocked/file/path.md"