from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from runtime import PythonRuntime
from parser import CodeParser
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI(title="OllaRuntime API")

# Enable CORS for Electron/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runtime = PythonRuntime()
parser = CodeParser()

# Mount static files for the dashboard
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def get_dashboard():
    return FileResponse("index.html")

class ExecuteRequest(BaseModel):
    prompt: str

@app.post("/api/execute")
async def execute(request: ExecuteRequest):
    # In a real scenario, we would call Ollama here.
    # For now, we simulate Ollama generating code based on the prompt.
    # Example: "Define x = 10" -> LLM generates "x = 10"
    
    # Simulate Ollama response (Mocking for now)
    # real_llm_response = call_ollama(request.prompt)
    
    # For the POC, we assume the prompt IS the code or contains it
    code_blocks = parser.extract_code(request.prompt)
    if not code_blocks:
        # Fallback: Treat whole prompt as code if no blocks found
        code_blocks = [request.prompt]
    
    output = ""
    for block in code_blocks:
        result = runtime.execute(block)
        output += f"{result}\n"
    
    return {
        "output": output.strip(),
        "variables": runtime.get_variables()
    }

@app.on_event("shutdown")
def shutdown_event():
    runtime.terminate()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
