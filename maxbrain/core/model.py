from google.ai import generativelanguage as genai
from .prompt import maxbrain_prompt
from ..agents.calendar import calendar_agent

# Initialize model with system prompt
def initialize_model():
    try:
        # For production with actual API key
        model = genai.GenerativeModel(
            'gemini-1.5-pro',
            system_instruction=maxbrain_prompt["system_instruction"],
            # tools=[calendar_agent]  # Commented out due to compatibility issues
        )
        return model
    except Exception as e:
        print(f"Error initializing model: {str(e)}")
        # Return a mock model for development
        return MockModel()

# Mock model for development
class MockModel:
    def __init__(self):
        self.responses = {
            "hello": "Hello! I'm MaxBrain AI. How can I assist you today?",
            "help": "I can help you with various tasks like managing your calendar, organizing projects, and more.",
            "default": "I'm a mock version of MaxBrain AI. In the full version, I would provide more intelligent responses."
        }
    
    def start_chat(self):
        return MockChat(self.responses)

class MockChat:
    def __init__(self, responses):
        self.responses = responses
    
    def send_message_stream(self, message):
        # Find the appropriate response
        response = self.responses.get(message.lower(), self.responses["default"])
        
        # Split the response into chunks to simulate streaming
        words = response.split()
        chunks = []
        
        for i in range(0, len(words), 3):
            chunk = " ".join(words[i:i+3])
            chunks.append(MockChunk(chunk + " "))
        
        return chunks

class MockChunk:
    def __init__(self, text):
        self.text = text
        self.tools = []

# Live streaming conversation
def start_conversation(model, user_query):
    try:
        convo = model.start_chat()
        for chunk in convo.send_message_stream(user_query):
            yield chunk.text
            # Handle tool calls from chunk.tools if available
            if hasattr(chunk, 'tools') and chunk.tools:
                for tool_call in chunk.tools:
                    handle_tool_call(tool_call)
    except Exception as e:
        # Fallback for errors
        yield f"I encountered an error while processing your request. Error: {str(e)}"
        yield "\nI'm currently running in development mode without a valid API key."

def handle_tool_call(tool_call):
    # Implementation for handling tool calls
    tool_name = tool_call.name
    tool_params = tool_call.parameters
    
    # Logic to route tool calls to appropriate handlers
    pass