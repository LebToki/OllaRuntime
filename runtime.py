import code
import io
import json
import os
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime
from typing import Dict, List, Any, Optional

class PythonRuntime:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.output_buffer = io.StringIO()
        self.history: List[Dict[str, Any]] = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._init_environment()

    def _init_environment(self):
        """Initialize the runtime with helpful imports and utilities."""
        init_code = """
import math
import json
import os
import sys
from datetime import datetime
"""
        self.execute(init_code)

    def execute(self, code_str: str) -> Dict[str, Any]:
        """Execute code and return structured result."""
        # Clear buffer
        self.output_buffer = io.StringIO()
        timestamp = datetime.now().isoformat()
        
        # Handle multi-line input correctly
        lines = code_str.splitlines()
        
        success = True
        error_message = None
        
        try:
            with redirect_stdout(self.output_buffer), redirect_stderr(self.output_buffer):
                more_needed = False
                for line in lines:
                    # console.push returns True if more input is required (incomplete block)
                    more_needed = self.console.push(line)
                
                # If more input is needed, we have incomplete code
                if more_needed:
                    success = False
                    error_message = "Incomplete code block. More input required."
        except Exception as e:
            success = False
            error_message = str(e)
        
        output = self.output_buffer.getvalue().strip()
        
        # Add to history
        history_entry = {
            "timestamp": timestamp,
            "code": code_str,
            "output": output,
            "success": success,
            "error": error_message
        }
        self.history.append(history_entry)
        
        return {
            "output": output,
            "success": success,
            "error": error_message,
            "variables": self.get_variables()
        }

    def get_variables(self) -> Dict[str, Any]:
        """Get all user-defined variables in a JSON-serializable format."""
        vars_dict = {}
        for k, v in self.console.locals.items():
            if not k.startswith('__'):
                try:
                    # Basic check for serializability
                    json.dumps(v)
                    vars_dict[k] = v
                except:
                    # Try to get a string representation
                    try:
                        vars_dict[k] = str(v)
                    except:
                        vars_dict[k] = f"<{type(v).__name__} object>"
        return vars_dict

    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get execution history."""
        if limit:
            return self.history[-limit:]
        return self.history

    def reset(self):
        """Reset the runtime to initial state."""
        self.console = code.InteractiveConsole()
        self.history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._init_environment()

    def save_session(self, filepath: Optional[str] = None) -> str:
        """Save current session to file."""
        if filepath is None:
            filepath = f"session_{self.session_id}.json"
        
        session_data = {
            "session_id": self.session_id,
            "history": self.history,
            "variables": self.get_variables(),
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        return filepath

    def load_session(self, filepath: str) -> bool:
        """Load session from file."""
        try:
            with open(filepath, 'r') as f:
                session_data = json.load(f)
            
            self.session_id = session_data.get("session_id", datetime.now().strftime("%Y%m%d_%H%M%S"))
            self.history = session_data.get("history", [])
            
            # Re-execute all history to restore state
            for entry in self.history:
                if entry.get("success"):
                    self.execute(entry["code"])
            
            return True
        except Exception as e:
            print(f"Error loading session: {e}")
            return False

    def get_variable_details(self, var_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific variable."""
        if var_name not in self.console.locals:
            return None
        
        var = self.console.locals[var_name]
        var_type = type(var).__name__
        
        details = {
            "name": var_name,
            "type": var_type,
            "value": None,
            "size": None,
            "attributes": []
        }
        
        try:
            details["value"] = str(var)
            json.dumps(var)  # Check if serializable
            details["serializable"] = True
        except:
            details["serializable"] = False
        
        # Get size for certain types
        if hasattr(var, '__len__'):
            try:
                details["size"] = len(var)
            except:
                pass
        
        # Get attributes for objects
        if hasattr(var, '__dict__'):
            details["attributes"] = list(var.__dict__.keys())
        
        return details

    def execute_file(self, filepath: str) -> Dict[str, Any]:
        """Execute a Python file."""
        try:
            with open(filepath, 'r') as f:
                code_content = f.read()
            return self.execute(code_content)
        except Exception as e:
            return {
                "output": "",
                "success": False,
                "error": f"Error reading file: {str(e)}",
                "variables": {}
            }

    def terminate(self):
        """Clean up resources."""
        self.console = None
        self.history = []
