from runtime import PythonRuntime
import json

def test_persistence():
    """Test that variables persist across executions."""
    runtime = PythonRuntime()
    print("=" * 50)
    print("TEST 1: Variable Persistence")
    print("=" * 50)
    
    print("\nStep 1: Setting x = 42")
    res1 = runtime.execute("x = 42")
    print(f"Output: {res1['output']}")
    print(f"Success: {res1['success']}")
    
    print("\nStep 2: Printing x")
    res2 = runtime.execute("print(x)")
    print(f"Output: {res2['output']}")
    print(f"Success: {res2['success']}")
    
    if "42" in res2['output']:
        print("\n✅ Persistence Test Passed!")
    else:
        print("\n❌ Persistence Test Failed!")
    
    runtime.terminate()

def test_function_definition():
    """Test function definition and execution."""
    runtime = PythonRuntime()
    print("\n" + "=" * 50)
    print("TEST 2: Function Definition")
    print("=" * 50)
    
    print("\nStep 1: Defining fibonacci function")
    res1 = runtime.execute("""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""")
    print(f"Success: {res1['success']}")
    
    print("\nStep 2: Calling fibonacci(10)")
    res2 = runtime.execute("print(fibonacci(10))")
    print(f"Output: {res2['output']}")
    print(f"Success: {res2['success']}")
    
    if "55" in res2['output']:
        print("\n✅ Function Definition Test Passed!")
    else:
        print("\n❌ Function Definition Test Failed!")
    
    runtime.terminate()

def test_history():
    """Test execution history tracking."""
    runtime = PythonRuntime()
    print("\n" + "=" * 50)
    print("TEST 3: Execution History")
    print("=" * 50)
    
    runtime.execute("a = 1")
    runtime.execute("b = 2")
    runtime.execute("c = a + b")
    
    history = runtime.get_history()
    print(f"\nTotal history entries: {len(history)}")
    
    for i, entry in enumerate(history, 1):
        print(f"\nEntry {i}:")
        print(f"  Code: {entry['code'][:50]}...")
        print(f"  Success: {entry['success']}")
        print(f"  Timestamp: {entry['timestamp']}")
    
    if len(history) == 3:
        print("\n✅ History Test Passed!")
    else:
        print("\n❌ History Test Failed!")
    
    runtime.terminate()

def test_variables():
    """Test variable inspection."""
    runtime = PythonRuntime()
    print("\n" + "=" * 50)
    print("TEST 4: Variable Inspection")
    print("=" * 50)
    
    runtime.execute("name = 'OllaRuntime'")
    runtime.execute("version = 2.0")
    runtime.execute("features = ['persistence', 'history', 'sessions']")
    
    variables = runtime.get_variables()
    print(f"\nVariables found: {list(variables.keys())}")
    
    for name, value in variables.items():
        print(f"  {name} = {value}")
    
    if 'name' in variables and 'version' in variables and 'features' in variables:
        print("\n✅ Variable Inspection Test Passed!")
    else:
        print("\n❌ Variable Inspection Test Failed!")
    
    runtime.terminate()

def test_session_save_load():
    """Test session save and load functionality."""
    runtime = PythonRuntime()
    print("\n" + "=" * 50)
    print("TEST 5: Session Save/Load")
    print("=" * 50)
    
    print("\nStep 1: Creating session data")
    runtime.execute("test_var = 'session_test'")
    runtime.execute("test_num = 123")
    
    print("\nStep 2: Saving session")
    filepath = runtime.save_session("test_session.json")
    print(f"Saved to: {filepath}")
    
    print("\nStep 3: Resetting runtime")
    runtime.reset()
    variables_after_reset = runtime.get_variables()
    print(f"Variables after reset: {list(variables_after_reset.keys())}")
    
    print("\nStep 4: Loading session")
    success = runtime.load_session("test_session.json")
    print(f"Load success: {success}")
    
    variables_after_load = runtime.get_variables()
    print(f"Variables after load: {list(variables_after_load.keys())}")
    
    if 'test_var' in variables_after_load and 'test_num' in variables_after_load:
        print("\n✅ Session Save/Load Test Passed!")
    else:
        print("\n❌ Session Save/Load Test Failed!")
    
    runtime.terminate()
    
    # Cleanup
    import os
    if os.path.exists("test_session.json"):
        os.remove("test_session.json")

def test_multiline_code():
    """Test multi-line code execution."""
    runtime = PythonRuntime()
    print("\n" + "=" * 50)
    print("TEST 6: Multi-line Code")
    print("=" * 50)
    
    code = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

calc = Calculator()
result = calc.add(5, 3)
print(f"5 + 3 = {result}")
"""
    
    print("\nExecuting multi-line code...")
    res = runtime.execute(code)
    print(f"Output: {res['output']}")
    print(f"Success: {res['success']}")
    
    if "5 + 3 = 8" in res['output']:
        print("\n✅ Multi-line Code Test Passed!")
    else:
        print("\n❌ Multi-line Code Test Failed!")
    
    runtime.terminate()

def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("OLLARUNTIME TEST SUITE v2.0")
    print("=" * 50)
    
    try:
        test_persistence()
        test_function_definition()
        test_history()
        test_variables()
        test_session_save_load()
        test_multiline_code()
        
        print("\n" + "=" * 50)
        print("ALL TESTS COMPLETED!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()
