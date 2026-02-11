from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from runtime import PythonRuntime
from parser import CodeParser
import uvicorn
import os

app = FastAPI(
    title="OllaRuntime API",
    description="Persistent Python Execution Layer for Ollama",
    version="2.0.0"
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

class ExecuteFileRequest(BaseModel):
    filepath: str

class SaveSessionRequest(BaseModel):
    filepath: Optional[str] = None

class LoadSessionRequest(BaseModel):
    filepath: str

@app.post("/api/execute")
async def execute(request: ExecuteRequest):
    """Execute code from a prompt. Extracts code blocks or treats prompt as code."""
    code_blocks = parser.extract_code(request.prompt)
    if not code_blocks:
        # Fallback: Treat whole prompt as code if no blocks found
        code_blocks = [request.prompt]
    
    results = []
    for block in code_blocks:
        result = runtime.execute(block)
        results.append(result)
    
    # Return the last result's output and current variables
    last_result = results[-1] if results else {"output": "", "success": True, "error": None}
    
    return {
        "output": last_result["output"],
        "success": last_result["success"],
        "error": last_result["error"],
        "variables": runtime.get_variables(),
        "session_id": runtime.session_id
    }

@app.post("/api/execute-file")
async def execute_file(request: ExecuteFileRequest):
    """Execute a Python file."""
    result = runtime.execute_file(request.filepath)
    return {
        "output": result["output"],
        "success": result["success"],
        "error": result["error"],
        "variables": runtime.get_variables()
    }

@app.get("/api/variables")
async def get_variables():
    """Get all current variables in the runtime."""
    return {
        "variables": runtime.get_variables(),
        "session_id": runtime.session_id
    }

@app.get("/api/variables/{var_name}")
async def get_variable_details(var_name: str):
    """Get detailed information about a specific variable."""
    details = runtime.get_variable_details(var_name)
    if details is None:
        raise HTTPException(status_code=404, detail=f"Variable '{var_name}' not found")
    return details

@app.get("/api/history")
async def get_history(limit: Optional[int] = None):
    """Get execution history."""
    return {
        "history": runtime.get_history(limit),
        "total": len(runtime.history)
    }

@app.post("/api/reset")
async def reset_runtime():
    """Reset the runtime to initial state."""
    runtime.reset()
    return {
        "message": "Runtime reset successfully",
        "session_id": runtime.session_id
    }

@app.post("/api/session/save")
async def save_session(request: SaveSessionRequest):
    """Save current session to file."""
    try:
        filepath = runtime.save_session(request.filepath)
        return {
            "message": "Session saved successfully",
            "filepath": filepath
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/session/load")
async def load_session(request: LoadSessionRequest):
    """Load session from file."""
    success = runtime.load_session(request.filepath)
    if success:
        return {
            "message": "Session loaded successfully",
            "session_id": runtime.session_id
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to load session")

@app.get("/api/session/info")
async def get_session_info():
    """Get current session information."""
    return {
        "session_id": runtime.session_id,
        "history_count": len(runtime.history),
        "variable_count": len(runtime.get_variables())
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "runtime": "OllaRuntime",
        "version": "2.0.0"
    }

@app.on_event("shutdown")
def shutdown_event():
    runtime.terminate()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
