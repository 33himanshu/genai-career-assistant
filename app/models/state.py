from typing import TypedDict, Optional, List, Dict, Any
from langchain_core.messages import BaseMessage

class State(TypedDict):
    """State model for the workflow graph."""
    query: str
    category: str
    response: str

class ChatHistory(TypedDict):
    """Chat history for interactive sessions."""
    messages: List[Dict[str, str]]
