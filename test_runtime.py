import unittest
import time
from runtime import PythonRuntime, SandboxError

class TestPythonRuntime(unittest.TestCase):
    def setUp(self):
        self.runtime = PythonRuntime()

    def tearDown(self):
        self.runtime.terminate()

    def test_basic_execution(self):
        result = self.runtime.execute("x = 10")
        self.assertEqual(result.strip(), "")
        result = self.runtime.execute("print(x * 2)")
        self.assertIn("20", result)

    def test_persistence(self):
        self.runtime.execute("y = 42")
        result = self.runtime.execute("print(y)")
        self.assertIn("42", result)

    def test_variable_serialization(self):
        self.runtime.execute("z = 'hello'")
        self.runtime.execute("w = [1, 2, 3]")
        variables = self.runtime.get_variables()
        self.assertIn("z", variables)
        self.assertIn("w", variables)
        self.assertEqual(variables["z"], "hello")
        self.assertEqual(variables["w"], [1, 2, 3])

    def test_security_restrictions(self):
        # Test import restrictions
        result = self.runtime.execute("import os")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("import sys")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("import subprocess")
        self.assertIn("Security Error", result)

        # Test dangerous functions
        result = self.runtime.execute("open('test.txt', 'w')")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("exec('print(1)')")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("eval('1+1')")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("del x")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("assert False")
        self.assertIn("Security Error", result)

        result = self.runtime.execute("raise Exception('test')")
        self.assertIn("Security Error", result)

    def test_syntax_errors(self):
        result = self.runtime.execute("print('hello")
        self.assertIn("Syntax Error", result)

    def test_runtime_errors(self):
        result = self.runtime.execute("1/0")
        self.assertIn("Runtime Error", result)

    def test_empty_input(self):
        result = self.runtime.execute("")
        self.assertEqual(result.strip(), "")

    def test_multiple_lines(self):
        result = self.runtime.execute("a = 1\nb = 2\nprint(a + b)")
        self.assertIn("3", result)

    def test_private_attributes(self):
        result = self.runtime.execute("_private = 10")
        self.assertIn("Security Error", result)

if __name__ == "__main__":
    unittest.main()
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
