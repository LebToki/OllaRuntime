# Screenshot Guide for OllaRuntime v2.0

This guide explains how to take screenshots of the OllaRuntime dashboard for documentation purposes.

## Prerequisites
- Python 3.10+ installed
- OllaRuntime running locally
- A screenshot tool (see options below)

## Taking Screenshots

### Option 1: Using Built-in Tools

#### macOS
```bash
# Full screen screenshot
Cmd + Shift + 3

# Select area screenshot
Cmd + Shift + 4
```

#### Windows
```bash
# Full screen screenshot
Win + Print Screen

# Snipping Tool
Win + Shift + S
```

#### Linux
```bash
# Using gnome-screenshot
gnome-screenshot

# Using scrot
scrot screenshot.png

# Using import (ImageMagick)
import -window root screenshot.png
```

### Option 2: Using Python (Automated)

Create a script `take_screenshot.py`:

```python
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def take_screenshot(url, output_file):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(2)  # Wait for page to load
        
        # Execute some code to populate the UI
        input_field = driver.find_element(By.ID, 'user-input')
        input_field.send_keys('x = 42\nprint(f"Hello from OllaRuntime! x = {x}")')
        
        # Find and click execute button
        execute_btn = driver.find_element(By.ID, 'execute-btn')
        execute_btn.click()
        
        time.sleep(1)  # Wait for execution
        
        driver.save_screenshot(output_file)
        print(f"Screenshot saved to {output_file}")
    finally:
        driver.quit()

if __name__ == "__main__":
    take_screenshot('http://localhost:8000', 'preview.png')
```

### Option 3: Using Playwright (Python)

```python
from playwright.sync_api import sync_playwright

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8000')
        page.screenshot(path='preview.png', full_page=True)
        browser.close()

if __name__ == "__main__":
    take_screenshot()
```

## Recommended Screenshot Content

For the best documentation screenshots, include:

1. **Terminal Tab with Active Execution**
   - Show some code being executed
   - Display output in the terminal
   - Show variables in the memory inspector

2. **History Tab**
   - Show multiple past executions
   - Display different types of code (functions, variables, etc.)

3. **Sessions Tab**
   - Show session management UI
   - Display save/load functionality

4. **Full Dashboard**
   - Capture the entire interface
   - Show all tabs and navigation

## Screenshot Best Practices

1. **Resolution:** Use at least 1920x1080 for clear text
2. **Dark Mode:** The dashboard is designed for dark mode
3. **Content:** Populate with meaningful code examples
4. **Consistency:** Use the same browser and settings for all screenshots
5. **File Format:** PNG for quality, WebP for size optimization

## Example Code for Screenshots

Use this code to populate the dashboard before taking screenshots:

```python
# Variable definitions
name = "OllaRuntime"
version = 2.0
features = ["persistence", "history", "sessions"]

# Function definition
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Data analysis
import statistics
data = [23, 45, 67, 89, 12, 34, 56, 78, 90, 11]
mean = statistics.mean(data)
print(f"Mean: {mean:.2f}")
```

## Uploading Screenshots

After taking screenshots:

1. Place the image in the project root as `preview.png`
2. Or upload to a service like:
   - GitHub (add to repo)
   - Imgur
   - Cloudinary
3. Update the README.md with the correct URL

## Current Status

The README currently references a placeholder image:
```
![OllaRuntime Dashboard](https://raw.githubusercontent.com/LebToki/OllaRuntime/main/preview.png)
```

Replace this with your actual screenshot URL.
