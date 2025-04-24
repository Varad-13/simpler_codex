# Simpler Codex

Simpler Codex is a Windows‐first conversational codebase assistant that uses OpenAI’s GPT API to read and update your project via PowerShell scripts.

## Features

- Interactive PowerShell loop for code updates  
- Automatically respects `.gitignore`  
- Generates `codebase_context.txt` with code and recent Git log  
- Emits `apply_updates.ps1` for you to run and apply changes  
- Creates Git commits with clear messages  

## Prerequisites

- Windows PowerShell  
- Python 3.8 or higher  
- Git installed and initialized in the project directory  
- An OpenAI API key  

## Installation

1. Clone the repo:  
   `git clone https://github.com/your-username/simpler-codex.git`  
2. Install dependencies:  
   `pip install openai`  

## Usage

1. Set your OpenAI key:  
   `setx OPENAI_API_KEY "your_key_here"`  
2. Launch the assistant:  
   `python codebase_assistant.py`  
3. In another PowerShell window, apply updates when prompted:  
   `.\apply_updates.ps1`  

## Troubleshooting

- Ensure at least one initial Git commit exists.  
- If script execution is blocked, run:  
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`  

## License

MIT License.
