from google.ai import generativelanguage as genai
from .prompt import maxbrain_prompt
from ..agents.calendar import calendar_agent

# Initialize model with system prompt
def initialize_model():
    model = genai.GenerativeModel(
        'gemini-1.5-pro',
        system_instruction=maxbrain_prompt["system_instruction"],
        tools=[calendar_agent]
    )
    return model

# Live streaming conversation
def start_conversation(model, user_query):
    convo = model.start_chat()
    for chunk in convo.send_message_stream(user_query):
        yield chunk.text
        # Handle tool calls from chunk.tools if available
        if hasattr(chunk, 'tools') and chunk.tools:
            for tool_call in chunk.tools:
                handle_tool_call(tool_call)

def handle_tool_call(tool_call):
    # Implementation for handling tool calls
    tool_name = tool_call.name
    tool_params = tool_call.parameters
    
    # Logic to route tool calls to appropriate handlers
    pass