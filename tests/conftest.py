import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.config import GOOGLE_API_KEY

@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def mock_google_llm():
    """Mock the Google Generative AI model responses."""
    with patch("langchain_google_genai.ChatGoogleGenerativeAI") as mock_llm:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value.content = "Mocked response"
        mock_llm.return_value = mock_instance
        yield mock_llm

@pytest.fixture
def mock_duckduckgo():
    """Mock the DuckDuckGo search results."""
    with patch("langchain_community.tools.DuckDuckGoSearchResults") as mock_search:
        mock_instance = MagicMock()
        mock_instance.invoke.return_value = "Mocked search results"
        mock_search.return_value = mock_instance
        yield mock_search

@pytest.fixture
def mock_file_utils():
    """Mock the file utility functions."""
    with patch("app.utils.file_utils.save_file") as mock_save:
        mock_save.return_value = "mocked/file/path.md"
        yield mock_save

@pytest.fixture
def sample_queries():
    """Sample queries for different categories."""
    return {
        "learning": "What are the basics of generative AI?",
        "resume": "Help me create a resume for an AI engineer position",
        "interview": "What questions should I prepare for a machine learning interview?",
        "mock_interview": "Can you conduct a mock interview for a Generative AI role?",
        "job_search": "Find AI engineer jobs in San Francisco"
    }

@pytest.fixture
def api_key_env():
    """Ensure API key is set for tests."""
    original_key = os.environ.get("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = "test_api_key"
    yield
    if original_key:
        os.environ["GOOGLE_API_KEY"] = original_key
    else:
        del os.environ["GOOGLE_API_KEY"]