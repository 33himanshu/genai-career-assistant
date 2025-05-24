from typing import Dict, Any, List, Optional
import time
import random
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults

from app.config import GOOGLE_API_KEY, GEMINI_PRO_MODEL
from app.utils.file_utils import save_file

class InterviewAgent:
    """Agent for interview preparation assistance."""
    
    def __init__(self):
        """Initialize the interview agent."""
        self.model = ChatGoogleGenerativeAI(
            model=GEMINI_PRO_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7
        )
        self.search_tool = DuckDuckGoSearchResults()
        self.use_fallback = False
    
    def _fallback_response(self, query: str) -> str:
        """Generate a fallback response when API limits are reached.
        
        Args:
            query: The user's query
            
        Returns:
            A fallback response
        """
        fallback_responses = [
            "Tell me about your experience with machine learning frameworks.",
            "How would you approach building a generative AI model from scratch?",
            "What challenges have you faced in previous AI projects?",
            "How do you stay updated with the latest developments in AI?",
            "Can you explain the difference between supervised and unsupervised learning?",
            "What metrics would you use to evaluate a generative model?",
            "How would you handle bias in AI systems?",
            "Tell me about a time when you had to debug a complex AI model."
        ]
        
        return f"Let's continue with the interview. {random.choice(fallback_responses)}"
    
    def generate_interview_questions(self, query: str) -> Dict[str, str]:
        """Generate interview questions based on the user's query.
        
        Args:
            query: The user's query about interview topics
            
        Returns:
            A dictionary containing the generated questions and file path
        """
        try:
            prompt = ChatPromptTemplate.from_template(
                "You are an expert interviewer for tech and AI positions. "
                "I need you to generate a comprehensive list of interview questions "
                "based on the following request:\n\n"
                "{query}\n\n"
                "Here's some information I found from a web search that might be helpful:\n"
                "{search_results}\n\n"
                "Please provide a well-structured set of interview questions with brief explanations "
                "of what the interviewer is looking for in the answers. Format your response in markdown."
            )
            
            search_results = self.search_tool.invoke(f"interview questions {query}")
            
            chain = prompt | self.model
            response = chain.invoke({
                "query": query,
                "search_results": search_results
            })
            
            content = response.content
        except Exception as e:
            print(f"API error: {str(e)}")
            self.use_fallback = True
            
            # Fallback content for interview questions
            content = f"""# Interview Questions for {query}

## Technical Questions
1. **What is your experience with generative AI models?**
   - *Looking for: Understanding of different architectures and hands-on experience*

2. **Explain the difference between GPT, BERT, and T5 models.**
   - *Looking for: Technical knowledge of transformer architectures*

3. **How would you handle bias in a language model?**
   - *Looking for: Awareness of ethical considerations and practical approaches*

## Problem-Solving Questions
1. **How would you design a system to generate realistic images from text descriptions?**
   - *Looking for: System design skills and understanding of multimodal models*

2. **What metrics would you use to evaluate a generative model?**
   - *Looking for: Knowledge of evaluation frameworks beyond simple accuracy*

## Behavioral Questions
1. **Tell me about a time when you had to explain a complex AI concept to non-technical stakeholders.**
   - *Looking for: Communication skills and ability to translate technical concepts*

2. **How do you stay updated with the latest developments in AI?**
   - *Looking for: Continuous learning mindset and professional development*
"""
        
        file_path = save_file(
            content=content,
            filename=f"interview_questions_{query.replace(' ', '_')[:30]}",
            extension="md"
        )
        
        return {
            "content": content,
            "file_path": file_path
        }
    
    def conduct_mock_interview(self, query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, str]:
        """Conduct a mock interview session based on the user's query.
        
        Args:
            query: The user's query about the mock interview
            chat_history: Optional list of previous chat messages
            
        Returns:
            A dictionary containing the response content and role
        """
        # If API limits have been reached, use fallback responses
        if self.use_fallback:
            return {
                "content": self._fallback_response(query),
                "role": "assistant"
            }
            
        try:
            # If this is the first message (no chat history), create a mock interview script
            if not chat_history:
                prompt = ChatPromptTemplate.from_template(
                    "You are an expert interviewer for tech and AI positions. "
                    "I need you to start a mock interview based on the following request:\n\n"
                    "{query}\n\n"
                    "Please respond as the interviewer with your first question. "
                    "Keep your response concise and focused on starting the interview."
                )
                
                chain = prompt | self.model
                response = chain.invoke({"query": query})
                
                return {
                    "content": response.content,
                    "role": "assistant"
                }
            
            # If we have chat history, continue the interview
            else:
                # Format the chat history for the model
                formatted_history = ""
                for msg in chat_history:
                    role = "Interviewer" if msg["role"] == "assistant" else "Candidate"
                    formatted_history += f"{role}: {msg['content']}\n\n"
                
                prompt = ChatPromptTemplate.from_template(
                    "You are conducting a mock interview for a tech or AI position. "
                    "Here's the conversation so far:\n\n"
                    "{formatted_history}\n\n"
                    "The candidate just said: {query}\n\n"
                    "Please respond as the interviewer. You can ask follow-up questions, "
                    "provide feedback, or move on to a new topic. Keep your response concise and realistic."
                )
                
                chain = prompt | self.model
                response = chain.invoke({
                    "formatted_history": formatted_history,
                    "query": query
                })
                
                return {
                    "content": response.content,
                    "role": "assistant"
                }
        except Exception as e:
            print(f"API error: {str(e)}")
            self.use_fallback = True
            
            return {
                "content": self._fallback_response(query),
                "role": "assistant"
            }

