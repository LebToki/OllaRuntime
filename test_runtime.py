from runtime import PythonRuntime
import time

def test_persistence():
    runtime = PythonRuntime()
    print("Step 1: Setting x = 42")
    res1 = runtime.execute("x = 42")
    print(f"Output: {res1}")
    
    print("\nStep 2: Printing x")
    res2 = runtime.execute("print(x)")
    print(f"Output: {res2}")
    
    if "42" in res2:
        print("\n✅ Persistence Test Passed!")
    else:
        print("\n❌ Persistence Test Failed!")
    
    runtime.terminate()

if __name__ == "__main__":
    test_persistence()
