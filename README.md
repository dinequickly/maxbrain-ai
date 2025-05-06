# MaxBrain AI

MaxBrain AI is an agentic operating system that serves as:
1. **Cognitive Assistant** - Externalized second brain
2. **Executive Function** - Orchestrator of skill agents
3. **Creative Partner** - Ideation engine
4. **Wellness Coach** - Biometric-aware helper

## Getting Started

### Prerequisites

- Python 3.9+
- Google AI API key (for Gemini model access)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/dinequickly/maxbrain-ai.git
cd maxbrain-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google AI API key:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### Running MaxBrain

#### Web Interface

```bash
streamlit run streamlit_app.py
```

This will start the Streamlit web interface. You can access it at http://localhost:8501

#### CLI Mode

```bash
python -m maxbrain.main --mode cli
```

This will start MaxBrain in command-line interface mode.

### Streamlit Cloud Deployment

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select this repository
4. Set the main file path to `streamlit_app.py`
5. Add the following secrets in the Streamlit Cloud dashboard:
   - `GOOGLE_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

## Project Structure

```
maxbrain/
├── core/               # Core system components
│   ├── prompt.py       # System prompts for the AI model
│   └── model.py        # Model initialization and interaction
├── agents/             # Skill agents
│   ├── calendar.py     # Calendar management agent
│   └── project.py      # Project management agent
├── memory/             # Memory management
│   └── vector_store.py # Vector storage for memories
├── frontend/           # User interfaces
│   └── app.py          # Streamlit web application
└── main.py             # Main entry point
```

## Features

- **Memory-Augmented Responses**: Retrieves relevant context from past interactions
- **Tool Calling**: Executes actions through specialized skill agents
- **Project Management**: Breaks down projects into research, design, and execution phases
- **Streaming Interface**: Real-time response generation

## Development

### Adding a New Skill Agent

1. Create a new file in the `agents/` directory
2. Define your agent using the Google AI Tool format
3. Implement the necessary functions
4. Register your agent in `core/model.py`

### Extending Memory Capabilities

The current implementation uses a simplified memory store. For production use, you should:

1. Set up Supabase with pgvector
2. Update the `memory/vector_store.py` file to connect to your database
3. Implement proper embedding generation using a suitable model

## License

[MIT License](LICENSE)
