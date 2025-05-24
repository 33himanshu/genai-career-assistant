import pytest
from unittest.mock import patch, MagicMock

from app.workflows.graph import categorize, handle_learning_resource, handle_interview_preparation
from app.workflows.graph import handle_resume_making, job_search, tutorial_agent, ask_query_bot
from app.workflows.graph import interview_topics_questions, mock_interview
from app.workflows.graph import route_query, route_interview, route_learning, create_workflow

def test_categorize(mock_google_llm, api_key_env):
    """Test the categorize function."""
    mock_google_llm.return_value.invoke.return_value.content = "1"
    result = categorize({"query": "What is generative AI?"})
    assert result == {"category": "1"}

def test_handle_learning_resource(mock_google_llm, api_key_env):
    """Test the handle_learning_resource function."""
    mock_google_llm.return_value.invoke.return_value.content = "Tutorial"
    result = handle_learning_resource({"query": "How to create a tutorial on generative AI?"})
    assert result == {"category": "Tutorial"}

def test_handle_interview_preparation(mock_google_llm, api_key_env):
    """Test the handle_interview_preparation function."""
    mock_google_llm.return_value.invoke.return_value.content = "Mock"
    result = handle_interview_preparation({"query": "Can you conduct a mock interview?"})
    assert result == {"category": "Mock"}

def test_route_query():
    """Test the route_query function."""
    assert route_query({"category": "1"}) == "handle_learning_resource"
    assert route_query({"category": "2"}) == "handle_resume_making"
    assert route_query({"category": "3"}) == "handle_interview_preparation"
    assert route_query({"category": "4"}) == "job_search"
    assert route_query({"category": "invalid"}) is None

def test_route_interview():
    """Test the route_interview function."""
    assert route_interview({"category": "Question"}) == "interview_topics_questions"
    assert route_interview({"category": "Mock"}) == "mock_interview"
    assert route_interview({"category": "invalid"}) == "mock_interview"  # Default case

def test_route_learning():
    """Test the route_learning function."""
    assert route_learning({"category": "Question"}) == "ask_query_bot"
    assert route_learning({"category": "Tutorial"}) == "tutorial_agent"
    assert route_learning({"category": "invalid"}) is None

def test_create_workflow():
    """Test the create_workflow function."""
    workflow = create_workflow()
    assert workflow is not None