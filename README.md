# 🚀 OllaRuntime v2.0

**Persistent Execution Layer for Ollama**

OllaRuntime adds "hands" to Ollama's "brain." It provides a persistent, stateful local execution environment (REPL) that allows Ollama-generated code to maintain variables, functions, and context across multiple independent prompts.

![OllaRuntime Dashboard](preview.svg)

*Note: This is an SVG preview. For a real screenshot, run the application and capture it using the [Screenshot Guide](SCREENSHOT_GUIDE.md).*

## 🧠 The Problem
Ollama is a powerful inference engine, but it is natively stateless. Each request to an LLM like Llama 3 or DeepSeek is an isolated event. If you ask it to "Define a variable `x = 10`" and then "Multiply `x` by 2," the model loses the context of `x` between calls unless you manually manage complex history and shell environments.

## ✨ The Solution: OllaRuntime v2.0
OllaRuntime bridges this gap by providing a persistent Python `InteractiveConsole` wrapped in a FastAPI backend with a premium glassmorphic dashboard.

### 🎯 Key Features

#### Core Features
- **Persistent State:** Variables, imported modules, and defined functions stay in memory across executions
- **FastAPI Bridge:** RESTful API for easy integration with any application
- **Premium UI:** High-contrast, glassmorphic dashboard with real-time monitoring
- **Docker-Less:** Lightweight and easy to run locally without container overhead

#### New in v2.0
- **📦 Session Management:** Save and load complete runtime sessions to/from JSON files
- **📜 Execution History:** Track all code executions with timestamps and results
- **🎨 Syntax Highlighting:** Beautiful code highlighting using highlight.js
- **📁 File Execution:** Execute Python files directly from the dashboard
- **🔍 Variable Inspection:** Detailed view of all variables in memory
- **🔄 Multi-line Code Support:** Proper handling of complex code blocks
- **⚡ Enhanced Error Handling:** Clear error messages and status indicators
- **📊 Session Info:** Real-time session statistics and metadata

## 🛠️ Use Cases
1. **Iterative Data Science:** Load a dataset once, then perform multiple follow-up analysis steps without re-loading
2. **Autonomous Coding Agents:** Build agents that can verify their own code by running it and seeing output/errors persistently
3. **Persistent Tooling:** Create custom REPL-based tools where the LLM can "learn" and store utility functions
4. **Educational Sandboxes:** Provide a safe, visual way for users to see how LLMs interact with real code execution
5. **Session Persistence:** Save your work and resume later exactly where you left off

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running (optional, for LLM integration)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/LebToki/OllaRuntime.git
    cd OllaRuntime
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running OllaRuntime
1. Start the backend:
    ```bash
    python main.py
    ```
2. Open your browser to `http://localhost:8000`

### Running Tests
```bash
python test_runtime.py
```

### Running the Demo
```bash
# Start the server in one terminal
python main.py

# Run the demo in another terminal
python demo.py
```

## 📖 API Documentation

### Execute Code
```http
POST /api/execute
Content-Type: application/json

{
  "prompt": "x = 42\nprint(x)"
}
```

### Execute Python File
```http
POST /api/execute-file
Content-Type: application/json

{
  "filepath": "path/to/script.py"
}
```

### Get Variables
```http
GET /api/variables
```

### Get Variable Details
```http
GET /api/variables/{var_name}
```

### Get Execution History
```http
GET /api/history?limit=10
```

### Reset Runtime
```http
POST /api/reset
```

### Save Session
```http
POST /api/session/save
Content-Type: application/json

{
  "filepath": "my_session.json"
}
```

### Load Session
```http
POST /api/session/load
Content-Type: application/json

{
  "filepath": "my_session.json"
}
```

### Get Session Info
```http
GET /api/session/info
```

### Health Check
```http
GET /api/health
```

## 🎨 Dashboard Features

### Terminal Tab
- Execute Python code directly
- View real-time output
- Syntax highlighted code display
- Clear terminal and reset session buttons

### History Tab
- View all past executions
- See execution status (success/error)
- Copy code from history
- Clear history option

### Sessions Tab
- Save current session to file
- Load previously saved sessions
- Session management UI

### Files Tab
- Execute Python files
- File path input
- Execution status feedback

### Memory Inspector
- Real-time variable display
- Variable count badge
- Click to inspect details
- Formatted value display

## 🏗️ Technical Architecture

### Backend
- **Framework:** FastAPI
- **Runtime:** Python `code.InteractiveConsole`
- **Session Management:** JSON-based persistence
- **Error Handling:** Comprehensive exception handling

### Frontend
- **Framework:** Vanilla JavaScript
- **Styling:** Custom CSS with glassmorphism
- **Syntax Highlighting:** highlight.js
- **Icons:** Unicode characters

### Pre-loaded Modules
The runtime comes with these modules pre-imported:
- `math` - Mathematical functions
- `json` - JSON encoding/decoding
- `os` - Operating system interface
- `sys` - System-specific parameters
- `datetime` - Date and time handling

## 📁 Project Structure
```
OllaRuntime/
├── main.py              # FastAPI application and API endpoints
├── runtime.py           # Python runtime implementation
├── parser.py            # Code extraction from markdown
├── index.html           # Dashboard UI
├── script.js            # Frontend JavaScript
├── style.css            # Dashboard styling
├── test_runtime.py      # Test suite
├── demo.py              # Feature demonstration script
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── plan.md              # Project planning document
```

## 🔒 Security Considerations

⚠️ **Important:** OllaRuntime executes code directly on your machine. In production:

1. **Sandbox the Runtime:** Use containers, VMs, or sandboxing tools like Firejail
2. **Network Restrictions:** Disable or restrict network access
3. **Resource Limits:** Set CPU and memory limits
4. **Authentication:** Add authentication to the API endpoints
5. **Input Validation:** Validate all code before execution

## 🤝 Contributing
Contributions are welcome! Areas for improvement:
- Add support for Node.js, Rust, or other runtimes
- Improve the UI with more features
- Add more robust sandboxing
- Implement authentication/authorization
- Add more pre-loaded utilities
- Create plugins/extensions system

## 📝 Changelog

### v2.0.0 (Current)
- ✨ Added session management (save/load)
- ✨ Added execution history tracking
- ✨ Added syntax highlighting
- ✨ Added file execution support
- ✨ Enhanced error handling
- ✨ Improved multi-line code support
- ✨ Added variable inspection
- ✨ Redesigned UI with tabs
- ✨ Added session info endpoint
- ✨ Added health check endpoint

### v1.0.0
- 🎉 Initial release
- Basic persistent Python runtime
- Simple web dashboard
- Variable inspection

## 📄 License
MIT License - feel free to use this project for any purpose.

## 🙏 Acknowledgments
- Built with ❤️ for the Ollama Community
- Inspired by the need for persistent LLM execution environments
- UI design inspired by modern glassmorphism trends

---
**"CASHFLOW OVER CLOUT" - 2T Interactive.**

## 📞 Support
- Open an issue on GitHub for bugs or feature requests
- Check the [Issues](https://github.com/LebToki/OllaRuntime/issues) page for known issues
- Join the discussion in the [Discussions](https://github.com/LebToki/OllaRuntime/discussions) section
