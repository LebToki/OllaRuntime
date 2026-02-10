Ollama is amazing on windows but lacks persistent compilers or runtimes natively—it's strictly an LLM inference engine. However, you can build a persistent execution layer around Ollama using external tooling.

Here are the practical approaches:

1. The Wrapper Architecture (Recommended)

Keep Ollama for generation, but maintain the compiler/runtime separately:


            
        
    
┌─────────────┐     generates code      ┌──────────────────────┐
│   Ollama    │ ──────────────────────> │  Persistent Runtime  │
│  (LLM)      │ <────────────────────── │ (Docker/VM/Process)  │
└─────────────┘     returns output      └──────────────────────┘
Implementation options:


Docker will make it more complex what if we build a complete framework that integrates with Ollama and this way we can buzz on reddit, x, github too.
I'm sure devs would love to be able to code/build and run within the free/ecosystem (open-source)
Keep a the app running with Python/Node/Rust/etc., send Ollama's generated code to it via API, maintain state in the container
Local process: Spawn a persistent REPL (Python, IPython, Node) and pipe Ollama outputs to it
Jupyter kernels: Use Jupyter's execution backend with Ollama as the "brain"

---

2. Tool Use / Function Calling (New in Ollama)

Recent Ollama versions support function calling. You can define a "execute_code" tool that sends code to your persistent environment:
        
            
        
    
{
  "tools": [{
    "type": "function",
    "function": {
      "name": "execute_python",
      "parameters": {
        "code": "string",
        "session_id": "string"  // For persistence
      }
    }
  }]
}
Your application maintains the Python process/session externally, while Ollama decides what code to run.

---

3. Projects That Already Do This

Instead of building from scratch:

Open Interpreter: Uses Ollama (or other LLMs) with a persistent local code environment

Continue.dev: VS Code extension with Ollama support that maintains execution context

LangChain/LlamaIndex: Frameworks to chain Ollama with persistent tool execution

---

4. What Won't Work


Modelfiles: You can't FROM llama3.2 and add a compiler—the Modelfile is for model parameters, not system dependencies

Ollama's built-in /api/generate: Each call is stateless; there's no "memory" of previous code executions unless you manage the conversation history yourself

---

## Security Warning

If you make this persistent, sandbox it. Never let an LLM execute generated code directly on your host machine. Use:

restricted networking
Firejail/seccomp
Temporary VMs
gVisor or similar sandboxing

Bottom line: Ollama handles the "brain" (LLM inference). You need to build or integrate the "hands" (compiler/runtime) separately, managing persistence at the application layer.