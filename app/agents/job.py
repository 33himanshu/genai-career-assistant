from typing import List, Dict, Any
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults

from app.config import GOOGLE_API_KEY, GEMINI_PRO_MODEL, USE_MOCK_RESPONSES
from app.utils.file_utils import save_file

class JobSearch:
    """Agent for job search assistance."""
    
    def __init__(self):
        """Initialize the job search agent."""
        # Initialize the chat model and search tools
        self.model = ChatGoogleGenerativeAI(
            model=GEMINI_PRO_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
        self.search_tool = DuckDuckGoSearchResults()
        self.use_fallback = USE_MOCK_RESPONSES
        
    def _fallback_response(self, query: str) -> str:
        """Generate a fallback response when API limits are reached."""
        job_locations = ["San Francisco", "New York", "Seattle", "Austin", "Remote"]
        companies = ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Startup Inc."]
        
        return f"""# Job Search Results for: {query}

## Top Opportunities

### 1. Senior Software Engineer - AI/ML
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $120,000 - $180,000  
**Description:** Looking for an experienced software engineer with expertise in machine learning and AI systems. The ideal candidate will have experience with large language models and generative AI applications.

### 2. Machine Learning Engineer
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $110,000 - $160,000  
**Description:** Join our team building next-generation AI products. You'll work on training and deploying models that power our core products.

### 3. AI Research Scientist
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $130,000 - $190,000  
**Description:** Research role focused on advancing the state of the art in generative AI. PhD in Computer Science, Machine Learning, or related field preferred.

### 4. Full Stack Developer with AI Experience
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $100,000 - $150,000  
**Description:** Looking for developers who can build end-to-end applications that leverage AI capabilities. Experience with React, Node.js, and Python required.

## Job Search Tips
- Update your resume to highlight AI/ML skills and projects
- Network with professionals in the field through LinkedIn and industry events
- Consider contributing to open-source AI projects to build your portfolio
- Prepare for technical interviews by practicing machine learning concepts and coding challenges

*Note: These job listings are examples based on your search query. For the most current opportunities, visit job boards like LinkedIn, Indeed, or company career pages.*
"""
        
    def find_jobs(self, query: str) -> Dict[str, str]:
        """Search for jobs based on the user's query.
        
        Args:
            query: The user's job search query
            
        Returns:
            A dictionary containing the search results and file path
        """
        # If we're in testing mode or have hit API limits before, use fallback
        if self.use_fallback:
            content = self._fallback_response(query)
            file_path = save_file(
                content=content,
                filename=f"job_search_{query.replace(' ', '_')[:30]}",
                extension="md"
            )
            
            return {
                "content": content,
                "file_path": file_path
            }
            
        try:
            # Create a prompt for job search
            prompt = ChatPromptTemplate.from_template(
                "You are a helpful job search assistant. I'll provide you with a job search query, "
                "and you'll help me find relevant job listings.\n\n"
                "Here's some information I found from a web search that might be helpful:\n"
                "{search_results}\n\n"
                "Based on this information, please provide a detailed list of job opportunities "
                "that match my search criteria. Include job titles, companies, locations, "
                "and brief descriptions when available. Format your response in markdown.\n\n"
                "My job search query is: {query}"
            )
            
            # Perform the search
            search_results = self.search_tool.invoke(f"job listings {query}")
            
            # Generate the response
            chain = prompt | self.model
            response = chain.invoke({
                "query": query,
                "search_results": search_results
            })
            
            content = response.content
        except Exception as e:
            print(f"API error: {str(e)}")
            self.use_fallback = True
            content = self._fallback_response(query)
        
        # Save the response to a file
        file_path = save_file(
            content=content,
            filename=f"job_search_{query.replace(' ', '_')[:30]}",
            extension="md"
        )
        
        return {
            "content": content,
            "file_path": file_path
        }


