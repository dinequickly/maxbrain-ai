import streamlit as st
import time
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from maxbrain.core.model import initialize_model, start_conversation
from maxbrain.memory.vector_store import MemoryStore
from maxbrain.agents.project import ProjectAgent

# Initialize memory store
memory_store = MemoryStore()

# Set up the Streamlit page
st.set_page_config(
    page_title="MaxBrain AI",
    page_icon="🧠",
    layout="wide",
)

# Add CSS for styling
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'projects' not in st.session_state:
    st.session_state.projects = {}
if 'model' not in st.session_state:
    try:
        st.session_state.model = initialize_model()
    except Exception as e:
        st.error(f"Error initializing model: {str(e)}")
        st.session_state.model = None

# App title
st.title("MaxBrain AI")
st.subheader("Your Cognitive Assistant & Executive Function System")

# Sidebar for projects and settings
with st.sidebar:
    st.header("Active Projects")
    
    # Project creation
    new_project = st.text_input("New Project Name")
    project_goal = st.text_area("Project Goal", height=100)
    if st.button("Create Project") and new_project and project_goal:
        st.session_state.projects[new_project] = ProjectAgent(project_goal)
        st.success(f"Project '{new_project}' created!")
    
    # Project list
    if st.session_state.projects:
        selected_project = st.selectbox(
            "Select a project to work on:",
            options=list(st.session_state.projects.keys())
        )
        
        if selected_project:
            project = st.session_state.projects[selected_project]
            st.write(f"Goal: {project.goal}")
            
            if st.button("Execute Project Chain"):
                with st.spinner("Executing project phases..."):
                    results = project.execute_chain()
                st.success("Project phases completed!")
                st.json(results)
    
    st.header("Memory Management")
    memory_query = st.text_input("Search Memories")
    if memory_query:
        memories = memory_store.retrieve_context(memory_query)
        st.write("Relevant Memories:")
        st.write(memories)
    
    # Add a new memory
    new_memory = st.text_area("Add New Memory", height=100)
    memory_tags = st.text_input("Tags (comma separated)")
    
    if st.button("Save Memory") and new_memory:
        tags = [tag.strip() for tag in memory_tags.split(",")] if memory_tags else []
        memory_store.add_memory(new_memory, {"tags": tags, "timestamp": time.time()})
        st.success("Memory saved!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What can MaxBrain help you with today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get context from memory
    context = memory_store.retrieve_context(prompt)
    
    # Generate response
    with st.chat_message("assistant"):
        if st.session_state.model:
            message_placeholder = st.empty()
            full_response = ""
            
            # Format user context
            user_context = {
                "user_name": "User",  # Replace with actual user name
                "active_projects": ", ".join(st.session_state.projects.keys()),
                "last_interaction": "Just now",  # Replace with actual timestamp
                "context": context
            }
            
            try:
                # Stream the response
                for response_chunk in start_conversation(st.session_state.model, prompt):
                    full_response += response_chunk
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
                full_response = "I'm sorry, I encountered an error while processing your request."
                message_placeholder.markdown(full_response)
        else:
            st.error("Model not initialized. Please check your API configuration.")
            full_response = "Model not available. Please check the configuration."
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Save the interaction to memory
    memory_store.add_memory(
        f"User: {prompt}\nAssistant: {full_response}",
        {"type": "conversation", "timestamp": time.time()}
    )