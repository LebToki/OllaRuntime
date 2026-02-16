import os
from typing import Dict, Any

class Config:
    def __init__(self):
        self.settings: Dict[str, Any] = {
            "app": {
                "title": "OllaRuntime",
                "version": "1.0.0",
                "host": "0.0.0.0",
                "port": 8000,
                "debug": False,
                "log_level": "INFO"
            },
            "security": {
                "max_execution_time": 5,  # seconds
                "max_memory_usage": 100 * 1024 * 1024,  # 100MB
                "allowed_builtins": [
                    'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'divmod',
                    'enumerate', 'filter', 'float', 'hex', 'int', 'len', 'list',
                    'map', 'max', 'min', 'oct', 'ord', 'pow', 'print', 'range',
                    'repr', 'round', 'set', 'slice', 'sorted', 'str', 'sum',
                    'tuple', 'type', 'zip'
                ],
                "restricted_operations": [
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
            },
            "limits": {
                "max_code_length": 10000,
                "max_variables": 100,
                "max_nesting_depth": 10
            }
        }

    def get(self, section: str, key: str = None, default=None):
        if section in self.settings:
            if key:
                return self.settings[section].get(key, default)
            return self.settings[section]
        return default

    def update(self, section: str, key: str, value: Any):
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value

    def load_from_env(self):
        # Load configuration from environment variables
        for section, keys in self.settings.items():
            for key in keys:
                env_var = f"{section.upper()}_{key.upper()}"
                if env_var in os.environ:
                    self.settings[section][key] = os.environ[env_var]

config = Config()