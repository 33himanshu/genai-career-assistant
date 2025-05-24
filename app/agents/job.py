from typing import List, Dict, Any
import random
import asyncio
from contextlib import asynccontextmanager
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
**Apply:** [Click here to apply](https://careers.microsoft.com/ai-ml-engineer)  
**Source:** Company Career Page

### 2. Machine Learning Engineer
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $110,000 - $160,000  
**Description:** Join our team building next-generation AI products. You'll work on training and deploying models that power our core products.  
**Apply:** [Apply on LinkedIn](https://www.linkedin.com/jobs/ml-engineer)  
**Source:** LinkedIn

### 3. AI Research Scientist
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $130,000 - $190,000  
**Description:** Research role focused on advancing the state of the art in generative AI. PhD in Computer Science, Machine Learning, or related field preferred.  
**Apply:** [Apply on Indeed](https://www.indeed.com/ai-research-scientist)  
**Source:** Indeed

### 4. Full Stack Developer with AI Experience
**Company:** {random.choice(companies)}  
**Location:** {random.choice(job_locations)}  
**Salary Range:** $100,000 - $150,000  
**Description:** Looking for developers who can build end-to-end applications that leverage AI capabilities. Experience with React, Node.js, and Python required.  
**Apply:** [Apply on Glassdoor](https://www.glassdoor.com/full-stack-ai-developer)  
**Source:** Glassdoor

## Job Search Tips
- Update your resume to highlight AI/ML skills and projects
- Network with professionals in the field through LinkedIn and industry events
- Consider contributing to open-source AI projects to build your portfolio
- Prepare for technical interviews by practicing machine learning concepts and coding challenges

*Note: These job listings are examples based on your search query. For the most current opportunities, visit job boards like LinkedIn, Indeed, or company career pages.*
"""

    async def find_jobs_async(self, query: str) -> Dict[str, str]:
        """Search for jobs based on the user's query asynchronously."""
        try:
            if self.use_fallback:
                content = self._fallback_response(query)
            else:
                # Perform the search using async DuckDuckGo search
                search_results = await self.search_tool.ainvoke(f"job listings {query}")

                # Create a prompt for job search
                prompt = ChatPromptTemplate.from_template(
                    "You are a helpful job search assistant. I'll provide you with a job search query, "
                    "and you'll help me find relevant job listings.\n\n"
                    "Here's some information I found from a web search that might be helpful:\n"
                    "{search_results}\n\n"
                    "Based on this information, please provide a detailed list of job opportunities "
                    "that match my search criteria. Include:\n"
                    "1. Job titles\n"
                    "2. Companies\n"
                    "3. Locations\n"
                    "4. Brief descriptions\n"
                    "5. Application links (very important - if a direct application link is found in the search results)\n"
                    "6. Source website (e.g. LinkedIn, Indeed, Internshala, Naukri etc.)\n\n"
                    "Format your response in markdown and make sure to include clickable links when available. "
                    "For jobs without direct application links, include a link to the job search page on the source website.\n\n"
                    "My job search query is: {query}"
                )

                # Generate the response using the async chain
                chain = prompt | self.model
                response = await chain.ainvoke({
                    "query": query,
                    "search_results": search_results
                })
                
                content = response.content

        except Exception as e:
            print(f"Search error: {str(e)}")
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

    def find_jobs(self, query: str) -> Dict[str, str]:
        """Synchronous wrapper for job search. Prefer using find_jobs_async for async contexts."""
        try:
            return asyncio.run(self.find_jobs_async(query))
        except Exception as e:
            print(f"API error: {str(e)}")
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


