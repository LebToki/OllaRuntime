// DOM Elements
const terminalOutput = document.getElementById('terminal-output');
const userInput = document.getElementById('user-input');
const memoryList = document.getElementById('memory-variables');
const sessionIdEl = document.getElementById('session-id');
const varCountEl = document.getElementById('var-count');
const historyList = document.getElementById('history-list');
const sessionMessage = document.getElementById('session-message');
const fileMessage = document.getElementById('file-message');

// State
let currentSessionId = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSessionInfo();
    setupEventListeners();
    setupTabNavigation();
});

function setupEventListeners() {
    // Terminal input
    userInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            await executeCommand();
        }
    });

    // Execute button
    document.getElementById('execute-btn').addEventListener('click', async () => {
        await executeCommand();
    });

    // Reset session
    document.getElementById('reset-session').addEventListener('click', async () => {
        if (confirm('Are you sure you want to reset the session? All variables and history will be lost.')) {
            await resetSession();
        }
    });

    // Clear terminal
    document.getElementById('clear-term').addEventListener('click', () => {
        terminalOutput.innerHTML = '<div class="line system">>> Terminal cleared.</div>';
    });

    // Save session (header button)
    document.getElementById('save-session-btn').addEventListener('click', async () => {
        await saveSession();
    });

    // Session management
    document.getElementById('save-session').addEventListener('click', async () => {
        const filename = document.getElementById('session-filename').value.trim();
        await saveSession(filename || null);
    });

    document.getElementById('load-session').addEventListener('click', async () => {
        const filename = document.getElementById('load-session-filename').value.trim();
        if (filename) {
            await loadSession(filename);
        }
    });

    // File execution
    document.getElementById('execute-file').addEventListener('click', async () => {
        const filepath = document.getElementById('file-path').value.trim();
        if (filepath) {
            await executeFile(filepath);
        }
    });

    // Clear history
    document.getElementById('clear-history').addEventListener('click', async () => {
        if (confirm('Clear execution history?')) {
            historyList.innerHTML = '<div class="history-item empty">No execution history yet.</div>';
        }
    });
}

function setupTabNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabName = item.dataset.tab;
            
            // Update nav items
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            // Update tab contents
            tabContents.forEach(content => {
                content.classList.remove('active');
                if (content.id === `tab-${tabName}`) {
                    content.classList.add('active');
                }
            });

            // Load data for specific tabs
            if (tabName === 'history') {
                loadHistory();
            }
        });
    });
}

async function loadSessionInfo() {
    try {
        const response = await fetch('/api/session/info');
        const data = await response.json();
        currentSessionId = data.session_id;
        sessionIdEl.textContent = currentSessionId;
        varCountEl.textContent = data.variable_count;
    } catch (error) {
        console.error('Failed to load session info:', error);
    }
}

async function executeCommand() {
    const command = userInput.value.trim();
    if (!command) return;

    // Display user input
    appendLine(command, 'user');
    userInput.value = '';

    appendLine('Processing...', 'system');
    
    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: command })
        });
        const data = await response.json();
        
        // Remove processing message
        const processingMsg = terminalOutput.querySelector('.line.system:last-child');
        if (processingMsg && processingMsg.textContent.includes('Processing')) {
            processingMsg.remove();
        }
        
        if (data.output) {
            appendCodeOutput(data.output, data.success);
        }
        
        if (data.error) {
            appendLine(`Error: ${data.error}`, 'error');
        }
        
        if (data.variables) {
            updateVariables(data.variables);
        }
        
        if (data.session_id) {
            currentSessionId = data.session_id;
            sessionIdEl.textContent = currentSessionId;
        }
    } catch (error) {
        appendLine('Error connecting to backend.', 'error');
    }

    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

async function resetSession() {
    try {
        const response = await fetch('/api/reset', { method: 'POST' });
        const data = await response.json();
        
        terminalOutput.innerHTML = `
            <div class="line system">>> Session reset successfully.</div>
            <div class="line system">>> New session ID: ${data.session_id}</div>
            <div class="line system">>> Python 3.10.x connected. State ready.</div>
        `;
        
        memoryList.innerHTML = '<div class="var-item empty">No variables defined yet.</div>';
        varCountEl.textContent = '0';
        currentSessionId = data.session_id;
        sessionIdEl.textContent = currentSessionId;
        
        showSessionMessage('Session reset successfully!', 'success');
    } catch (error) {
        showSessionMessage('Failed to reset session.', 'error');
    }
}

async function saveSession(filename = null) {
    try {
        const response = await fetch('/api/session/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: filename })
        });
        const data = await response.json();
        showSessionMessage(`Session saved to: ${data.filepath}`, 'success');
    } catch (error) {
        showSessionMessage('Failed to save session.', 'error');
    }
}

async function loadSession(filename) {
    try {
        const response = await fetch('/api/session/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: filename })
        });
        const data = await response.json();
        
        showSessionMessage(`Session loaded successfully!`, 'success');
        currentSessionId = data.session_id;
        sessionIdEl.textContent = currentSessionId;
        
        // Refresh variables
        await refreshVariables();
    } catch (error) {
        showSessionMessage('Failed to load session. Check filename and try again.', 'error');
    }
}

async function executeFile(filepath) {
    try {
        const response = await fetch('/api/execute-file', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filepath: filepath })
        });
        const data = await response.json();
        
        if (data.output) {
            appendLine(`>> Executing file: ${filepath}`, 'system');
            appendCodeOutput(data.output, data.success);
        }
        
        if (data.error) {
            appendLine(`Error: ${data.error}`, 'error');
        }
        
        if (data.variables) {
            updateVariables(data.variables);
        }
        
        showFileMessage(`File executed successfully!`, 'success');
    } catch (error) {
        showFileMessage('Failed to execute file. Check path and try again.', 'error');
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        if (data.history.length === 0) {
            historyList.innerHTML = '<div class="history-item empty">No execution history yet.</div>';
            return;
        }
        
        historyList.innerHTML = '';
        data.history.forEach((entry, index) => {
            const item = document.createElement('div');
            item.className = 'history-item';
            item.innerHTML = `
                <div class="history-header">
                    <span class="history-index">#${index + 1}</span>
                    <span class="history-time">${formatTime(entry.timestamp)}</span>
                    <span class="history-status ${entry.success ? 'success' : 'error'}">
                        ${entry.success ? '✓' : '✗'}
                    </span>
                </div>
                <pre class="history-code"><code>${escapeHtml(entry.code)}</code></pre>
                ${entry.output ? `<div class="history-output">${escapeHtml(entry.output)}</div>` : ''}
                ${entry.error ? `<div class="history-error">${escapeHtml(entry.error)}</div>` : ''}
            `;
            historyList.appendChild(item);
        });
    } catch (error) {
        historyList.innerHTML = '<div class="history-item empty">Failed to load history.</div>';
    }
}

async function refreshVariables() {
    try {
        const response = await fetch('/api/variables');
        const data = await response.json();
        updateVariables(data.variables);
        varCountEl.textContent = Object.keys(data.variables).length;
    } catch (error) {
        console.error('Failed to refresh variables:', error);
    }
}

function appendLine(text, type) {
    const line = document.createElement('div');
    line.className = `line ${type}`;
    line.textContent = type === 'user' ? `λ ${text}` : text;
    terminalOutput.appendChild(line);
}

function appendCodeOutput(text, isSuccess) {
    const line = document.createElement('div');
    line.className = `line ${isSuccess ? 'code' : 'error'}`;
    
    // Try to syntax highlight if it looks like code
    if (text.includes('def ') || text.includes('class ') || text.includes('import ')) {
        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.className = 'language-python';
        code.textContent = text;
        pre.appendChild(code);
        line.appendChild(pre);
        hljs.highlightElement(code);
    } else {
        line.textContent = text;
    }
    
    terminalOutput.appendChild(line);
}

function updateVariables(variables) {
    memoryList.innerHTML = '';
    const vars = Object.entries(variables);
    varCountEl.textContent = vars.length;
    
    if (vars.length === 0) {
        memoryList.innerHTML = '<div class="var-item empty">No variables defined yet.</div>';
        return;
    }
    
    vars.forEach(([name, value]) => {
        const item = document.createElement('div');
        item.className = 'var-item';
        item.innerHTML = `
            <div class="var-name">${name}</div>
            <div class="var-value">${formatValue(value)}</div>
        `;
        item.addEventListener('click', () => showVariableDetails(name));
        memoryList.appendChild(item);
    });
}

function formatValue(value) {
    if (typeof value === 'string') {
        if (value.length > 50) {
            return `"${value.substring(0, 50)}..."`;
        }
        return `"${value}"`;
    }
    if (Array.isArray(value)) {
        return `[${value.length} items]`;
    }
    if (typeof value === 'object' && value !== null) {
        return `{${Object.keys(value).length} keys}`;
    }
    return String(value);
}

function showVariableDetails(varName) {
    // For now, just log to console - could expand to show a modal
    console.log(`Variable details for: ${varName}`);
}

function showSessionMessage(message, type) {
    sessionMessage.textContent = message;
    sessionMessage.className = `session-message ${type}`;
    setTimeout(() => {
        sessionMessage.textContent = '';
        sessionMessage.className = 'session-message';
    }, 3000);
}

function showFileMessage(message, type) {
    fileMessage.textContent = message;
    fileMessage.className = `session-message ${type}`;
    setTimeout(() => {
        fileMessage.textContent = '';
        fileMessage.className = 'session-message';
    }, 3000);
}

function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
