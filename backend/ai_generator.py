import google.generativeai as genai
from typing import List, Optional, Dict, Any

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
    
    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model, system_instruction=self.SYSTEM_PROMPT)
        
    def generate_response(self, query: str,
                         conversation_history: Optional[str] = None,
                         tools: Optional[List] = None,
                         tool_manager=None) -> str:
        """
        Generate AI response with optional tool usage and conversation context.
        
        Args:
            query: The user's question or request
            conversation_history: Previous messages for context
            tools: Available tools the AI can use
            tool_manager: Manager to execute tools
            
        Returns:
            Generated response as string
        """
        
        chat = self.model.start_chat()
        
        # Add conversation history to the chat
        if conversation_history:
            # The Gemini API expects a list of Content objects
            # We need to parse the string history into this format
            # Assuming history is a simple string, we can't easily reconstruct the full conversation
            # For now, we will just send the last user message
            # A better implementation would store the history in a more structured way
            pass

        # Send the user's query to the model
        response = chat.send_message(query, tools=tools)
        
        # Handle tool execution if needed
        if response.function_calls and tool_manager:
            return self._handle_tool_execution(response, chat, tool_manager)
        
        # Return direct response
        return response.text
    
    def _handle_tool_execution(self, initial_response, chat, tool_manager):
        """
        Handle execution of tool calls and get follow-up response.
        
        Args:
            initial_response: The response containing tool use requests
            chat: The chat object
            tool_manager: Manager to execute tools
            
        Returns:
            Final response text after tool execution
        """
        
        # Execute the function call
        function_call = initial_response.function_calls[0]
        tool_result = tool_manager.execute_tool(
            function_call.name, 
            **function_call.args
        )
        
        # Send the tool result back to the model
        response = chat.send_message(
            part=genai.Part(
                function_response=genai.FunctionResponse(
                    name=function_call.name,
                    response=tool_result,
                ),
            ),
        )
        
        return response.text
