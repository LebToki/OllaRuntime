import code
import io
import sys
import traceback
import time
import resource
from contextlib import redirect_stdout, redirect_stderr
from types import SimpleNamespace
from config import config

class SandboxError(Exception):
    pass

class RestrictedEnvironment:
    def __init__(self):
        self.locals = {
            '__builtins__': {
                'abs': abs,
                'all': all,
                'any': any,
                'bin': bin,
                'bool': bool,
                'chr': chr,
                'dict': dict,
                'divmod': divmod,
                'enumerate': enumerate,
                'filter': filter,
                'float': float,
                'hex': hex,
                'int': int,
                'len': len,
                'list': list,
                'map': map,
                'max': max,
                'min': min,
                'oct': oct,
                'ord': ord,
                'pow': pow,
                'print': print,
                'range': range,
                'repr': repr,
                'round': round,
                'set': set,
                'slice': slice,
                'sorted': sorted,
                'str': str,
                'sum': sum,
                'tuple': tuple,
                'type': type,
                'zip': zip,
            },
            '__name__': '__main__',
            '__doc__': None,
            '__package__': None
        }

    def __getitem__(self, key):
        return self.locals.get(key)

    def __setitem__(self, key, value):
        if key.startswith('_'):
            raise SandboxError(f"Access to private attributes is restricted: {key}")
        self.locals[key] = value

    def __contains__(self, key):
        return key in self.locals

class PythonRuntime:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.output_buffer = io.StringIO()
        self.environment = RestrictedEnvironment()
        self.max_execution_time = config.get("security", "max_execution_time", 5)
        self.max_memory_usage = config.get("security", "max_memory_usage", 100 * 1024 * 1024)
        self.max_variables = config.get("limits", "max_variables", 100)
        self.max_nesting_depth = config.get("limits", "max_nesting_depth", 10)

    def _set_resource_limits(self):
        # Set CPU time limit
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (self.max_execution_time, self.max_execution_time))
        except (ValueError, AttributeError):
            pass  # Resource limits not supported on this platform

        # Set memory limit (if supported)
        try:
            if self.max_memory_usage > 0:
                resource.setrlimit(resource.RLIMIT_AS, (self.max_memory_usage, self.max_memory_usage))
        except (ValueError, AttributeError):
            pass  # Resource limits not supported on this platform

    def _validate_code(self, code_str):
        # Check for dangerous patterns
        for pattern in config.get("security", "restricted_operations", []):
            if re.search(pattern, code_str, re.IGNORECASE):
                raise SandboxError(f"Restricted operation detected: {pattern}")

        # Check nesting depth
        nesting_level = self._calculate_nesting_level(code_str)
        if nesting_level > self.max_nesting_depth:
            raise SandboxError(f"Code nesting depth exceeds limit: {nesting_level} > {self.max_nesting_depth}")

        # Check variable count
        if self._count_variables(code_str) > self.max_variables:
            raise SandboxError(f"Too many variables in code")

    def _calculate_nesting_level(self, code_str):
        max_depth = 0
        current_depth = 0
        for char in code_str:
            if char in '({[':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in ')}]':
                current_depth -= 1
        return max_depth

    def _count_variables(self, code_str):
        # Simple variable count heuristic
        import re
        variables = re.findall(r'\b\w+\b(?=\s*=)', code_str)
        return len(set(variables))
    def execute(self, code_str: str):
        # Clear buffer
        self.output_buffer = io.StringIO()

        try:
            # Check code length
            if len(code_str) > config.get("limits", "max_code_length", 10000):
                raise SandboxError("Code exceeds maximum allowed length")

            # Parse and validate code
            self._validate_code(code_str)

            # Set resource limits
            self._set_resource_limits()

            start_time = time.time()
            with redirect_stdout(self.output_buffer), redirect_stderr(self.output_buffer):
                # Execute in restricted environment
                self._execute_in_sandbox(code_str)

            execution_time = time.time() - start_time
            if execution_time > self.max_execution_time:
                raise SandboxError(f"Execution time exceeded: {execution_time:.2f}s")

            return self.output_buffer.getvalue().strip()
        except SandboxError as e:
            return f"Security Error: {str(e)}"
        except SyntaxError as e:
            return f"Syntax Error: {str(e)}"
        except Exception as e:
            return f"Runtime Error: {str(e)}\n{traceback.format_exc()}"

    def _validate_code(self, code_str):
        # Check for dangerous patterns
        for pattern in config.get("security", "restricted_operations", []):
            if re.search(pattern, code_str, re.IGNORECASE):
                raise SandboxError(f"Restricted operation detected: {pattern}")

    def _execute_in_sandbox(self, code_str):
        lines = code_str.splitlines()
        for line in lines:
            # Use restricted environment
            self.console.push(line)
            # Update environment with new variables
            for name, value in self.console.locals.items():
                if not name.startswith('__'):
                    self.environment[name] = value

    def get_variables(self):
        # Filter out built-ins and internal names, and ensure they are JSON serializable
        vars_dict = {}
        for k, v in self.environment.locals.items():
            if not k.startswith('__'):
                try:
                    import json
                    json.dumps(v)
                    vars_dict[k] = v
                except:
                    vars_dict[k] = f"<{type(v).__name__} object>"
        return vars_dict

    def terminate(self):
        pass # No process to kill
class SandboxError(Exception):
    pass

class RestrictedEnvironment:
    def __init__(self):
        self.locals = {
            '__builtins__': {
                'abs': abs,
                'all': all,
                'any': any,
                'bin': bin,
                'bool': bool,
                'chr': chr,
                'dict': dict,
                'divmod': divmod,
                'enumerate': enumerate,
                'filter': filter,
                'float': float,
                'hex': hex,
                'int': int,
                'len': len,
                'list': list,
                'map': map,
                'max': max,
                'min': min,
                'oct': oct,
                'ord': ord,
                'pow': pow,
                'print': print,
                'range': range,
                'repr': repr,
                'round': round,
                'set': set,
                'slice': slice,
                'sorted': sorted,
                'str': str,
                'sum': sum,
                'tuple': tuple,
                'type': type,
                'zip': zip,
            },
            '__name__': '__main__',
            '__doc__': None,
            '__package__': None
        }

    def __getitem__(self, key):
        return self.locals.get(key)

    def __setitem__(self, key, value):
        if key.startswith('_'):
            raise SandboxError(f"Access to private attributes is restricted: {key}")
        self.locals[key] = value

    def __contains__(self, key):
        return key in self.locals

class PythonRuntime:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.output_buffer = io.StringIO()
        self.environment = RestrictedEnvironment()

    def execute(self, code_str: str):
        # Clear buffer
        self.output_buffer = io.StringIO()

        try:
            # Parse and validate code
            self._validate_code(code_str)

            with redirect_stdout(self.output_buffer), redirect_stderr(self.output_buffer):
                # Execute in restricted environment
                self._execute_in_sandbox(code_str)

            return self.output_buffer.getvalue().strip()
        except SandboxError as e:
            return f"Security Error: {str(e)}"
        except SyntaxError as e:
            return f"Syntax Error: {str(e)}"
        except Exception as e:
            return f"Runtime Error: {str(e)}\n{traceback.format_exc()}"

    def _validate_code(self, code_str):
        # Check for dangerous patterns
        dangerous_patterns = [
            r'import\s+os',
            r'import\s+sys',
            r'import\s+subprocess',
            r'import\s+shutil',
            r'import\s+glob',
            r'import\s+pathlib',
            r'from\s+os',
            r'from\s+sys',
            r'from\s+subprocess',
            r'from\s+shutil',
            r'from\s+glob',
            r'from\s+pathlib',
            r'open\s*\(',
            r'exec\s*\(',
            r'eval\s*\(',
            r'compile\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'del\s+',
            r'assert\s+',
            r'raise\s+',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, code_str, re.IGNORECASE):
                raise SandboxError(f"Restricted operation detected: {pattern}")

    def _execute_in_sandbox(self, code_str):
        lines = code_str.splitlines()
        for line in lines:
            # Use restricted environment
            self.console.push(line)
            # Update environment with new variables
            for name, value in self.console.locals.items():
                if not name.startswith('__'):
                    self.environment[name] = value

    def get_variables(self):
        # Filter out built-ins and internal names, and ensure they are JSON serializable
        vars_dict = {}
        for k, v in self.environment.locals.items():
            if not k.startswith('__'):
                try:
                    import json
                    json.dumps(v)
                    vars_dict[k] = v
                except:
                    vars_dict[k] = f"<{type(v).__name__} object>"
        return vars_dict

    def terminate(self):
        pass # No process to kill
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
