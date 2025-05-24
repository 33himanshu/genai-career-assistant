import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(test_client):
    """Test the root endpoint returns the expected message."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "GenAI Career Assistant API is running"}

def test_workflow_endpoint(test_client, mock_google_llm, mock_file_utils, sample_queries, api_key_env):
    """Test the workflow endpoint with a learning query."""
    response = test_client.post(
        "/workflow",
        json={"query": sample_queries["learning"]}
    )
    assert response.status_code == 200
    assert "category" in response.json()
    assert "response" in response.json()

def test_learning_tutorial_endpoint(test_client, mock_google_llm, mock_duckduckgo, mock_file_utils, sample_queries, api_key_env):
    """Test the learning tutorial endpoint."""
    response = test_client.post(
        "/api/learning/tutorial",
        json={"query": sample_queries["learning"]}
    )
    assert response.status_code == 200
    assert "content" in response.json()
    assert "file_path" in response.json()

def test_learning_query_endpoint(test_client, mock_google_llm, sample_queries, api_key_env):
    """Test the learning query endpoint."""
    response = test_client.post(
        "/api/learning/query",
        json={"query": sample_queries["learning"]}
    )
    assert response.status_code == 200
    assert "content" in response.json()
    assert "role" in response.json()

def test_resume_create_endpoint(test_client, mock_google_llm, mock_duckduckgo, mock_file_utils, sample_queries, api_key_env):
    """Test the resume creation endpoint."""
    response = test_client.post(
        "/api/resume/create",
        json={"query": sample_queries["resume"]}
    )
    assert response.status_code == 200
    assert "content" in response.json()
    assert "file_path" in response.json()

def test_interview_questions_endpoint(test_client, mock_google_llm, mock_duckduckgo, mock_file_utils, sample_queries, api_key_env):
    """Test the interview questions endpoint."""
    response = test_client.post(
        "/api/interview/questions",
        json={"query": sample_queries["interview"]}
    )
    assert response.status_code == 200
    assert "content" in response.json()
    assert "file_path" in response.json()

def test_mock_interview_endpoint(test_client, mock_google_llm, sample_queries, api_key_env):
    """Test the mock interview endpoint."""
    response = test_client.post(
        "/api/interview/mock",
        json={"query": sample_queries["mock_interview"]}
    )
    assert response.status_code == 200
    assert "content" in response.json()
    assert "role" in response.json()

def test_job_search_endpoint(test_client, mock_google_llm, mock_duckduckgo, mock_file_utils, sample_queries, api_key_env):
    """Test the job search endpoint."""
    response = test_client.post(
        "/api/job/search",
        json={"query": sample_queries["job_search"]}
    )
    assert response.status_code == 200
    assert "content" in response.json()
    assert "file_path" in response.json()