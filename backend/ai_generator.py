import google.generativeai as genai
from typing import List, Optional, Dict, Any
from models import Message

class AIGenerator:
    """Handles interactions with Google's Gemini API for generating responses"""
    
    SYSTEM_PROMPT = """ You are an AI assistant specialized in course materials and educational content with access to a comprehensive search tool for course information.

Search Tool Usage:
- Use the search tool **only** for questions about specific course content or detailed educational materials
- **One search per query maximum**
- Synthesize search results into accurate, fact-based responses
- If search yields no results, state this clearly without offering alternatives

Response Protocol:
- **General knowledge questions**: Answer using existing knowledge without searching
- **Course-specific questions**: Search first, then answer
- **No meta-commentary**:
 - Provide direct answers only — no reasoning process, search explanations, or question-type analysis
 - Do not mention "based on the search results"


All responses must be:
1. **Brief, Concise and focused** - Get to the point quickly
2. **Educational** - Maintain instructional value
3. **Clear** - Use accessible language
4. **Example-supported** - Include relevant examples when they aid understanding
Provide only the direct answer to what was asked.
"""
    
    def __init__(self, api_key: str, model: str, tools: Optional[List] = None):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model, system_instruction=self.SYSTEM_PROMPT, tools=tools)
        
    def generate_response(self, query: str,
                         conversation_history: Optional[List[Message]] = None) -> str:
        """
        Generate AI response with optional tool usage and conversation context.
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            
        Returns:
            Generated response as string
        """
        
        history = []
        if conversation_history:
            for msg in conversation_history:
                role = "model" if msg.role == "assistant" else msg.role
                history.append({"role": role, "parts": [{"text": msg.content}]})
        
        chat = self.model.start_chat(history=history, enable_automatic_function_calling=True)

        # Send the user's query to the model
        response = chat.send_message(query)
        
        # Return direct response
        return response.text
