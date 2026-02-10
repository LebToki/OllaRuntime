import code
import io
from contextlib import redirect_stdout, redirect_stderr

class PythonRuntime:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.output_buffer = io.StringIO()

    def execute(self, code_str: str):
        # Clear buffer
        self.output_buffer = io.StringIO()
        
        # We need to handle multi-line input correctly
        lines = code_str.splitlines()
        
        with redirect_stdout(self.output_buffer), redirect_stderr(self.output_buffer):
            for line in lines:
                # console.push returns True if more input is required (incomplete block)
                self.console.push(line)
        
        return self.output_buffer.getvalue().strip()

    def get_variables(self):
        # Filter out built-ins and internal names, and ensure they are JSON serializable
        vars_dict = {}
        for k, v in self.console.locals.items():
            if not k.startswith('__'):
                try:
                    # Basic check for serializability
                    import json
                    json.dumps(v)
                    vars_dict[k] = v
                except:
                    vars_dict[k] = f"<{type(v).__name__} object>"
        return vars_dict

    def terminate(self):
        pass # No process to kill
