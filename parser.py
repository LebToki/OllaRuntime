import re

class CodeParser:
    def __init__(self):
        # Match markdown code blocks: ```python ... ``` or ``` ... ```
        self.code_block_re = re.compile(r'```(?:python|py)?\s*(.*?)```', re.DOTALL)

    def extract_code(self, text: str):
        matches = self.code_block_re.findall(text)
        if not matches:
            return []
        return [match.strip() for match in matches]
