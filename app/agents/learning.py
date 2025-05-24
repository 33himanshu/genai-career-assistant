from typing import Dict, Any
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults

from app.config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
from app.utils.file_utils import save_file

class LearningResourceAgent:
    """Agent for creating learning resources and answering queries about generative AI."""
    
    def __init__(self):
        """Initialize the learning resource agent."""
        self.model = ChatGoogleGenerativeAI(
            model=GEMINI_PRO_MODEL,
            google_api_key=GOOGLE_API_KEY
        )
        self.search_tool = DuckDuckGoSearchResults()
        self.use_fallback = False
    
    def _fallback_response(self, query: str) -> str:
        """Generate a fallback response when API limits are reached."""
        return f"""# Response to: {query}

## Overview
Generative AI refers to artificial intelligence systems that can generate new content, including text, images, audio, and more. These systems learn patterns from existing data and use that knowledge to create new, original content.

## Key Concepts
- **Neural Networks**: The foundation of modern AI systems
- **Transformers**: Architecture behind many language models
- **Training Data**: Critical for model performance and bias mitigation
- **Fine-tuning**: Adapting pre-trained models for specific tasks

## Applications
- Content creation
- Code generation
- Virtual assistants
- Creative tools for artists and designers

## Challenges
- Ethical considerations
- Bias in training data
- Computational requirements
- Evaluation metrics

For more information, consider exploring resources from organizations like OpenAI, Google AI, and academic institutions specializing in machine learning research.
"""
    
    def create_tutorial(self, query: str) -> Dict[str, str]:
        """Create a tutorial based on the user's query."""
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are an expert in generative AI and technical writing. "
                "I need you to create a comprehensive tutorial based on the following request:\n\n"
                "{query}\n\n"
                "Here's some information I found from a web search that might be helpful:\n"
                "{search_results}\n\n"
                "Please provide a well-structured tutorial with explanations, examples, and code snippets where appropriate. "
                "Format your response in markdown with clear headings, subheadings, and sections."
            )
            
            search_results = self.search_tool.invoke(f"tutorial {query}")
            
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
        
        file_path = save_file(
            content=content,
            filename=f"tutorial_{query.replace(' ', '_')[:30]}",
            extension="md"
        )
        
        return {
            "content": content,
            "file_path": file_path
        }
    
    def answer_query(self, query: str) -> Dict[str, str]:
        """Answer a query about generative AI."""
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are an expert in generative AI and related technologies. "
                "I have a question about generative AI that I need you to answer:\n\n"
                "{query}\n\n"
                "Here's some information I found from a web search that might be helpful:\n"
                "{search_results}\n\n"
                "Please provide a comprehensive and educational answer. "
                "Include examples and explanations where appropriate. Format your response in markdown."
            )
            
            search_results = self.search_tool.invoke(query)
            
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
        
        file_path = save_file(
            content=content,
            filename=f"answer_{query.replace(' ', '_')[:30]}",
            extension="md"
        )
        
        return {
            "content": content,
            "file_path": file_path
        }



