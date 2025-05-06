import os
import argparse
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("maxbrain.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("MaxBrain")

def setup_environment():
    """Set up the environment variables and dependencies"""
    try:
        # Check for Google AI API key
        if not os.environ.get("GOOGLE_API_KEY"):
            logger.warning("GOOGLE_API_KEY environment variable not set. Using mock mode.")
            # For development, you can set a mock key
            os.environ["GOOGLE_API_KEY"] = "mock_key_for_development"
        
        # Additional environment setup can go here
        logger.info("Environment setup complete")
    except Exception as e:
        logger.error(f"Error setting up environment: {str(e)}")
        raise

def run_web_interface(port=12000, debug=False):
    """Run the Streamlit web interface"""
    try:
        import streamlit.web.cli as stcli
        import sys
        
        # Set Streamlit configuration
        os.environ["STREAMLIT_SERVER_PORT"] = str(port)
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
        os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "true"
        os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
        
        # Run the Streamlit app
        sys.argv = [
            "streamlit", "run", 
            os.path.join(os.path.dirname(__file__), "frontend", "app.py"),
            "--server.port", str(port),
            "--server.address", "0.0.0.0",
            "--server.enableCORS", "true",
            "--server.enableXsrfProtection", "false"
        ]
        
        if debug:
            sys.argv.append("--logger.level=debug")
        
        logger.info(f"Starting Streamlit web interface on port {port}")
        stcli.main()
    except Exception as e:
        logger.error(f"Error running web interface: {str(e)}")
        raise

def run_cli_mode():
    """Run MaxBrain in CLI mode"""
    from maxbrain.core.model import initialize_model, start_conversation
    from maxbrain.memory.vector_store import MemoryStore
    
    try:
        logger.info("Initializing MaxBrain in CLI mode")
        
        # Initialize components
        memory_store = MemoryStore()
        model = initialize_model()
        
        print("\n===== MaxBrain AI CLI =====")
        print("Type 'exit' to quit\n")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            # Get context from memory
            context = memory_store.retrieve_context(user_input)
            
            print("\nMaxBrain: ", end="")
            full_response = ""
            
            # Stream the response
            for response_chunk in start_conversation(model, user_input):
                full_response += response_chunk
                print(response_chunk, end="", flush=True)
            
            print("\n")
            
            # Save the interaction to memory
            memory_store.add_memory(
                f"User: {user_input}\nAssistant: {full_response}",
                {"type": "conversation", "timestamp": datetime.now().timestamp()}
            )
    except Exception as e:
        logger.error(f"Error in CLI mode: {str(e)}")
        raise

def main():
    """Main entry point for MaxBrain"""
    parser = argparse.ArgumentParser(description="MaxBrain AI - Cognitive Assistant")
    parser.add_argument("--mode", choices=["web", "cli"], default="web", help="Run mode (web or cli)")
    parser.add_argument("--port", type=int, default=12000, help="Port for web interface")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    try:
        # Setup environment
        setup_environment()
        
        # Run in selected mode
        if args.mode == "web":
            run_web_interface(port=args.port, debug=args.debug)
        else:
            run_cli_mode()
    except Exception as e:
        logger.error(f"Error running MaxBrain: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())