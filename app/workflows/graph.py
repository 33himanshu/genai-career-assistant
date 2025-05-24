from typing import Dict, Any
# Updated imports for langgraph 0.1.0
from langgraph.graph import StateGraph
from langgraph.graph.graph import END, START
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from app.models.state import State
from app.config import GOOGLE_API_KEY, GEMINI_FLASH_MODEL
from app.agents.learning import LearningResourceAgent
from app.agents.interview import InterviewAgent
from app.agents.resume import ResumeMaker
from app.agents.job import JobSearch

# Initialize the LLM for categorization
llm = ChatGoogleGenerativeAI(
    model=GEMINI_FLASH_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5
)

def categorize(state: State) -> Dict[str, Any]:
    """Categorizes the user query into one of four main categories."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following customer query into one of these categories:\n"
        "1: Learn Generative AI Technology\n"
        "2: Resume Making\n"
        "3: Interview Preparation\n"
        "4: Job Search\n"
        "Give the number only as an output.\n\n"
        "Examples:\n"
        "1. Query: 'What are the basics of generative AI, and how can I start learning it?' -> 1\n"
        "2. Query: 'Can you help me improve my resume for a tech position?' -> 2\n"
        "3. Query: 'What are some common questions asked in AI interviews?' -> 3\n"
        "4. Query: 'Are there any job openings for AI engineers?' -> 4\n\n"
        "Now, categorize the following customer query:\n"
        "Query: {query}"
    )

    chain = prompt | llm
    category = chain.invoke({"query": state["query"]}).content
    return {"category": category}

def handle_learning_resource(state: State) -> Dict[str, Any]:
    """Determines if the query is related to Tutorial creation or general Questions."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following user query into one of these categories:\n\n"
        "Categories:\n"
        "- Tutorial: For queries related to creating tutorials, blogs, or documentation on generative AI.\n"
        "- Question: For general queries asking about generative AI topics.\n"
        "- Default to Question if the query doesn't fit either of these categories.\n\n"
        "Examples:\n"
        "1. User query: 'How to create a blog on prompt engineering for generative AI?' -> Category: Tutorial\n"
        "2. User query: 'Can you provide a step-by-step guide on fine-tuning a generative model?' -> Category: Tutorial\n"
        "3. User query: 'Provide me the documentation for Langchain?' -> Category: Tutorial\n"
        "4. User query: 'What are the main applications of generative AI?' -> Category: Question\n"
        "5. User query: 'Is there any generative AI course available?' -> Category: Question\n\n"
        "Now, categorize the following user query:\n"
        "The user query is: {query}\n"
    )

    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"category": response}

def handle_interview_preparation(state: State) -> Dict[str, Any]:
    """Determines if the query is related to Mock Interviews or general Interview Questions."""
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following user query into one of these categories:\n\n"
        "Categories:\n"
        "- Mock: For requests related to mock interviews.\n"
        "- Question: For general queries asking about interview topics or preparation.\n"
        "- Default to Question if the query doesn't fit either of these categories.\n\n"
        "Examples:\n"
        "1. User query: 'Can you conduct a mock interview with me for a Gen AI role?' -> Category: Mock\n"
        "2. User query: 'What topics should I prepare for an AI Engineer interview?' -> Category: Question\n"
        "3. User query: 'I need to practice interview focused on Gen AI.' -> Category: Mock\n"
        "4. User query: 'Can you list important coding topics for AI tech interviews?' -> Category: Question\n\n"
        "Now, categorize the following user query:\n"
        "The user query is: {query}\n"
    )

    chain = prompt | llm
    response = chain.invoke({"query": state["query"]}).content
    return {"category": response}

def route_query(state: State):
    """Route the query based on its category to the appropriate handler."""
    if '1' in state["category"]:
        return "handle_learning_resource"
    elif '2' in state["category"]:
        return "handle_resume_making"
    elif '3' in state["category"]:
        return "handle_interview_preparation"
    elif '4' in state["category"]:
        return "job_search"
    else:
        return None

def route_interview(state: State) -> str:
    """Route the query to the appropriate interview-related handler."""
    if 'Question'.lower() in state["category"].lower():
        return "interview_topics_questions"
    elif 'Mock'.lower() in state["category"].lower():
        return "mock_interview"
    else:
        return "mock_interview"  # Default to mock interview

def route_learning(state: State):
    """Route the query based on the learning path category."""
    if 'Question'.lower() in state["category"].lower():
        return "ask_query_bot"
    elif 'Tutorial'.lower() in state["category"].lower():
        return "tutorial_agent"
    else:
        return None

def create_workflow():
    """Create and return the workflow graph."""
    # Create the workflow graph
    workflow = StateGraph(State)

    # Add nodes for each state in the workflow
    workflow.add_node("categorize", categorize)
    workflow.add_node("handle_learning_resource", handle_learning_resource)
    workflow.add_node("handle_interview_preparation", handle_interview_preparation)
    workflow.add_node("handle_resume_making", handle_resume_making)  # Add this node
    workflow.add_node("job_search", job_search)  # Add this node
    workflow.add_node("mock_interview", mock_interview)  # Add this node
    workflow.add_node("interview_topics_questions", interview_topics_questions)  # Add this node
    workflow.add_node("tutorial_agent", tutorial_agent)  # Add this node
    workflow.add_node("ask_query_bot", ask_query_bot)  # Add this node

    # Define the starting edge to the categorization node
    workflow.add_edge(START, "categorize")

    # Add conditional edges based on category routing function
    workflow.add_conditional_edges(
        "categorize",
        route_query,
        {
            "handle_learning_resource": "handle_learning_resource",
            "handle_resume_making": "handle_resume_making",
            "handle_interview_preparation": "handle_interview_preparation",
            "job_search": "job_search"
        }
    )

    # Add conditional edges for further routing in interview preparation
    workflow.add_conditional_edges(
        "handle_interview_preparation",
        route_interview,
        {
            "mock_interview": "mock_interview",
            "interview_topics_questions": "interview_topics_questions",
        }
    )

    # Add conditional edges for further routing in learning resources
    workflow.add_conditional_edges(
        "handle_learning_resource",
        route_learning,
        {
            "tutorial_agent": "tutorial_agent",
            "ask_query_bot": "ask_query_bot",
        }
    )

    # Define edges that lead to the end of the workflow
    workflow.add_edge("handle_resume_making", END)
    workflow.add_edge("job_search", END)
    workflow.add_edge("interview_topics_questions", END)
    workflow.add_edge("mock_interview", END)
    workflow.add_edge("ask_query_bot", END)
    workflow.add_edge("tutorial_agent", END)

    # Set the initial entry point to start the workflow at the categorize node
    workflow.set_entry_point("categorize")

    # Compile the workflow graph into an application
    return workflow.compile()

def handle_resume_making(state: State) -> Dict[str, Any]:
    """Generate a customized resume based on user details for a tech role in AI and Generative AI."""
    from app.agents.resume import ResumeMaker
    
    agent = ResumeMaker()
    result = agent.create_resume(state["query"])
    
    return {"response": result["file_path"]}

def job_search(state: State) -> Dict[str, Any]:
    """Search for jobs based on user criteria."""
    from app.agents.job import JobSearch
    
    agent = JobSearch()
    result = agent.find_jobs(state["query"])
    
    return {"response": result["file_path"]}

def mock_interview(state: State) -> Dict[str, Any]:
    """Conduct a mock interview session."""
    from app.agents.interview import InterviewAgent
    
    agent = InterviewAgent()
    result = agent.conduct_mock_interview(state["query"])
    
    return {"response": result["content"]}

def interview_topics_questions(state: State) -> Dict[str, Any]:
    """Generate interview questions and topics."""
    from app.agents.interview import InterviewAgent
    
    agent = InterviewAgent()
    result = agent.generate_interview_questions(state["query"])
    
    return {"response": result["file_path"]}

def tutorial_agent(state: State) -> Dict[str, Any]:
    """Create a tutorial on a generative AI topic."""
    from app.agents.learning import LearningResourceAgent
    
    agent = LearningResourceAgent()
    result = agent.create_tutorial(state["query"])
    
    return {"response": result["file_path"]}

def ask_query_bot(state: State) -> Dict[str, Any]:
    """Answer a query about generative AI."""
    from app.agents.learning import LearningResourceAgent
    
    agent = LearningResourceAgent()
    result = agent.answer_query(state["query"])
    
    return {"response": result["file_path"]}





