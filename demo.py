"""
OllaRuntime Demo Script
This script demonstrates the key features of OllaRuntime v2.0
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_response(response):
    """Pretty print API response."""
    print(json.dumps(response.json(), indent=2))

def demo_basic_execution():
    """Demonstrate basic code execution."""
    print_section("1. Basic Code Execution")
    
    # Execute simple code
    response = requests.post(f"{BASE_URL}/api/execute", json={
        "prompt": "x = 42\nprint(f'The answer is {x}')"
    })
    print_response(response)
    time.sleep(1)

def demo_function_definition():
    """Demonstrate function definition and usage."""
    print_section("2. Function Definition")
    
    # Define a function
    response = requests.post(f"{BASE_URL}/api/execute", json={
        "prompt": """
def greet(name):
    return f'Hello, {name}! Welcome to OllaRuntime.'

print(greet('Developer'))
"""
    })
    print_response(response)
    time.sleep(1)

def demo_persistence():
    """Demonstrate variable persistence."""
    print_section("3. Variable Persistence")
    
    # Set a variable
    requests.post(f"{BASE_URL}/api/execute", json={
        "prompt": "counter = 0"
    })
    
    # Increment it multiple times
    for i in range(3):
        response = requests.post(f"{BASE_URL}/api/execute", json={
            "prompt": "counter += 1\nprint(f'Counter: {counter}')"
        })
        print(f"Increment {i+1}: {response.json()['output']}")
        time.sleep(0.5)

def demo_variables():
    """Demonstrate variable inspection."""
    print_section("4. Variable Inspection")
    
    # Create some variables
    requests.post(f"{BASE_URL}/api/execute", json={
        "prompt": """
name = 'OllaRuntime'
version = 2.0
features = ['persistence', 'history', 'sessions']
active = True
"""
    })
    
    # Get all variables
    response = requests.get(f"{BASE_URL}/api/variables")
    print_response(response)
    time.sleep(1)

def demo_history():
    """Demonstrate execution history."""
    print_section("5. Execution History")
    
    # Execute some code
    requests.post(f"{BASE_URL}/api/execute", json={"prompt": "a = 10"})
    requests.post(f"{BASE_URL}/api/execute", json={"prompt": "b = 20"})
    requests.post(f"{BASE_URL}/api/execute", json={"prompt": "c = a + b"})
    
    # Get history
    response = requests.get(f"{BASE_URL}/api/history")
    print(f"Total executions: {response.json()['total']}")
    for entry in response.json()['history']:
        print(f"  - {entry['code'][:40]}... [{entry['timestamp']}]")
    time.sleep(1)

def demo_session_management():
    """Demonstrate session save and load."""
    print_section("6. Session Management")
    
    # Create session data
    requests.post(f"{BASE_URL}/api/execute", json={
        "prompt": "session_data = 'This is important data'"
    })
    
    # Save session
    response = requests.post(f"{BASE_URL}/api/session/save", json={
        "filepath": "demo_session.json"
    })
    print(f"Session saved: {response.json()}")
    time.sleep(1)
    
    # Reset runtime
    requests.post(f"{BASE_URL}/api/reset")
    print("Runtime reset")
    time.sleep(1)
    
    # Load session
    response = requests.post(f"{BASE_URL}/api/session/load", json={
        "filepath": "demo_session.json"
    })
    print(f"Session loaded: {response.json()}")
    time.sleep(1)
    
    # Verify data
    response = requests.get(f"{BASE_URL}/api/variables")
    print(f"Variables after load: {list(response.json()['variables'].keys())}")

def demo_complex_operations():
    """Demonstrate complex operations."""
    print_section("7. Complex Operations")
    
    # Data analysis example
    response = requests.post(f"{BASE_URL}/api/execute", json={
        "prompt": """
import statistics

data = [23, 45, 67, 89, 12, 34, 56, 78, 90, 11]
mean = statistics.mean(data)
median = statistics.median(data)
stdev = statistics.stdev(data)

print(f'Data: {data}')
print(f'Mean: {mean:.2f}')
print(f'Median: {median}')
print(f'Std Dev: {stdev:.2f}')
"""
    })
    print_response(response)
    time.sleep(1)

def demo_session_info():
    """Demonstrate session info endpoint."""
    print_section("8. Session Information")
    
    response = requests.get(f"{BASE_URL}/api/session/info")
    print_response(response)

def demo_health_check():
    """Demonstrate health check."""
    print_section("9. Health Check")
    
    response = requests.get(f"{BASE_URL}/api/health")
    print_response(response)

def run_demo():
    """Run the complete demo."""
    print("\n" + "=" * 60)
    print("  OLLARUNTIME v2.0 - FEATURE DEMONSTRATION")
    print("=" * 60)
    print("\nMake sure the server is running:")
    print("  python main.py")
    print("\nStarting demo in 3 seconds...")
    time.sleep(3)
    
    try:
        demo_health_check()
        demo_basic_execution()
        demo_function_definition()
        demo_persistence()
        demo_variables()
        demo_history()
        demo_session_management()
        demo_complex_operations()
        demo_session_info()
        
        print("\n" + "=" * 60)
        print("  DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nOpen http://localhost:8000 in your browser to see the UI")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to OllaRuntime server.")
        print("Please make sure the server is running with: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    run_demo()
