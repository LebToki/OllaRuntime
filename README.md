# 🚀 OllaRuntime

**Persistent Execution Layer for Ollama**

OllaRuntime adds "hands" to Ollama's "brain." It provides a persistent, stateful local execution environment (REPL) that allows Ollama-generated code to maintain variables, functions, and context across multiple independent prompts.

![OllaRuntime Dashboard Preview](https://raw.githubusercontent.com/LebToki/OllaRuntime/main/preview.png) *(Placeholder for the preview image is being uploaded soon, promise)*

## 🧠 The Problem
Ollama is a powerful inference engine, but it is natively stateless. Each request to an LLM like Llama 3 or DeepSeek is an isolated event. If you ask it to "Define a variable `x = 10`" and then "Multiply `x` by 2," the model loses the context of `x` between calls unless you manually manage complex history and shell environments.

## ✨ The Solution: OllaRuntime
OllaRuntime bridges this gap by providing a persistent Python `InteractiveConsole` wrapped in a FastAPI backend. 

- **Persistent State:** Variables, imported modules, and defined functions stay in memory.
- **FastAPI Bridge:** Easy integration for any application wanting to add execution capabilities to Ollama.
- **Premium UI:** A high-contrast, glassmorphic dashboard for real-time monitoring of the execution state and memory.
- **Docker-Less:** Lightweight and easy to run locally on Windows/Linux/Mac without container overhead.

## 🛠️ Use Cases
1. **Iterative Data Science:** Ask Ollama to load a dataset, then perform multiple follow-up analysis steps without re-loading the data.
2. **Autonomous Coding Agents:** Build agents that can verify their own code by running it and seeing output/errors persistently.
3. **Persistent Tooling:** Create custom REPL-based tools where the LLM can "learn" and store utility functions over a long conversation.
4. **Educational Sandboxes:** Provide a safe, visual way for users to see how LLMs interact with real code execution.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/LebToki/OllaRuntime.git
   cd OllaRuntime
   ```
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

### Running OllaRuntime
1. Start the backend:
   ```bash
   python main.py
   ```
2. Open your browser to `http://localhost:8000`.

## 🏗️ Technical Architecture
- **Backend:** FastAPI (Python)
- **Runtime:** Persistent `code.InteractiveConsole`
- **Frontend:** Vanilla JS/CSS (Premium Glassmorphism)
- **Bridging:** Regex-based markdown code extraction
```
graph TD
    subgraph User_Interface ["Frontend (Vanilla JS/CSS)"]
        UI[Glassmorphic Dashboard]
    end

    subgraph Backend_Layer ["FastAPI Backend"]
        API[FastAPI Server]
        Extract[Regex Code Extractor]
    end

    subgraph Execution_Layer ["Stateful Runtime"]
        REPL[Persistent Python InteractiveConsole]
        Memory[(In-Memory State: Vars/Funcs)]
    end

    subgraph External
        Ollama[Ollama Local LLM]
    end

    UI <--> API
    API <--> Extract
    Extract <--> REPL
    REPL <--> Memory
    Ollama -- Generates Code --> API
    ```

## 🤝 Contributing
Contributions are welcome! Whether it's adding support for Node.js runtimes, improving the UI, or adding more robust sandboxing, feel free to open a PR.

---
Built with ❤️ for the Ollama Community. 
**"CASHFLOW OVER CLOUT" - 2T Interactive.**
