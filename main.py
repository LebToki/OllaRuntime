from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from runtime import PythonRuntime
from parser import CodeParser
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
import resource
from config import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.get("app", "log_level", "INFO")))
logger = logging.getLogger(__name__)

app = FastAPI(
    title=config.get("app", "title", "OllaRuntime"),
    version=config.get("app", "version", "1.0.0")
)
runtime = PythonRuntime()
parser = CodeParser()

# Mount static files for the dashboard
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def get_dashboard():
    return FileResponse("index.html")

class ExecuteRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=config.get("limits", "max_code_length", 10000), description="Code or prompt to execute")

@app.post("/api/execute")
async def execute(request: ExecuteRequest):
    try:
        # Validate request
        if not request.prompt.strip():
            return JSONResponse(status_code=400, content={"error": "Empty prompt"})

        # Extract code blocks
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
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Execution error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.on_event("shutdown")
def shutdown_event():
    runtime.terminate()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    logger.info(f"Starting {config.get('app', 'title', 'OllaRuntime')} server...")
    uvicorn.run(
        app,
        host=config.get("app", "host", "0.0.0.0"),
        port=config.get("app", "port", 8000),
        log_level=config.get("app", "log_level", "info")
    )
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OllaRuntime API", version="1.0.0")
runtime = PythonRuntime()
parser = CodeParser()

# Mount static files for the dashboard
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def get_dashboard():
    return FileResponse("index.html")

class ExecuteRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=10000, description="Code or prompt to execute")

@app.post("/api/execute")
async def execute(request: ExecuteRequest):
    try:
        # Validate request
        if not request.prompt.strip():
            return JSONResponse(status_code=400, content={"error": "Empty prompt"})

        # Extract code blocks
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
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Execution error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.on_event("shutdown")
def shutdown_event():
    runtime.terminate()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"}
    )

if __name__ == "__main__":
    logger.info("Starting OllaRuntime server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
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
