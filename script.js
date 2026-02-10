const terminalOutput = document.getElementById('terminal-output');
const userInput = document.getElementById('user-input');
const memoryList = document.getElementById('memory-variables');

userInput.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter') {
        const command = userInput.value.trim();
        if (!command) return;

        // Display user input
        appendLine(command, 'user');
        userInput.value = '';

        // TODO: Call backend API
        appendLine('Processing...', 'system');
        
        try {
            const response = await fetch('/api/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: command })
            });
            const data = await response.json();
            
            if (data.output) {
                appendLine(data.output, 'code');
            }
            if (data.variables) {
                updateVariables(data.variables);
            }
        } catch (error) {
            appendLine('Error connecting to backend.', 'system');
        }

        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
});

function appendLine(text, type) {
    const line = document.createElement('div');
    line.className = `line ${type}`;
    line.textContent = type === 'user' ? `λ ${text}` : text;
    terminalOutput.appendChild(line);
}

function updateVariables(variables) {
    memoryList.innerHTML = '';
    const vars = Object.entries(variables);
    if (vars.length === 0) {
        memoryList.innerHTML = '<div class="var-item empty">No variables defined yet.</div>';
        return;
    }
    vars.forEach(([name, value]) => {
        const item = document.createElement('div');
        item.className = 'var-item';
        item.textContent = `${name} = ${JSON.stringify(value)}`;
        memoryList.appendChild(item);
    });
}
