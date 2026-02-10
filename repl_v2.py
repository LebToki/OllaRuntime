import sys
import io
import code
from contextlib import redirect_stdout, redirect_stderr

class PersistentREPL:
    def __init__(self):
        self.console = code.InteractiveConsole()
        self.output_buffer = io.StringIO()

    def execute(self, code_str: str):
        # Clear buffer
        self.output_buffer = io.StringIO()
        
        with redirect_stdout(self.output_buffer), redirect_stderr(self.output_buffer):
            # Split code into lines to handle them correctly in the console
            lines = code_str.splitlines()
            for line in lines:
                self.console.push(line)
        
        return self.output_buffer.getvalue().strip()

    def get_variables(self):
        # Filter out built-ins and internal names
        return {k: v for k, v in self.console.locals.items() if not k.startswith('__')}

if __name__ == "__main__":
    # Test it
    repl = PersistentREPL()
    print("Exec 1: x = 10")
    repl.execute("x = 10")
    print("Exec 2: print(x * 2)")
    out = repl.execute("print(x * 2)")
    print(f"Output: {out}")
    print(f"Vars: {repl.get_variables()}")
