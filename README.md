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
git clone https://github.com/yourusername/maxbrain-ai.git
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
python -m maxbrain.main --mode web --port 12000
```

This will start the Streamlit web interface on port 12000. You can access it at http://localhost:12000

#### CLI Mode

```bash
python -m maxbrain.main --mode cli
```

This will start MaxBrain in command-line interface mode.

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