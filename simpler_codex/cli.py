import os
import platform
import subprocess
import openai
from pathlib import Path

CONTEXT_FILE = "codebase_context.txt"
UPDATE_SCRIPT = "apply_updates.ps1"
SYSTEM_PROMPT = """You are an AI code assistant that helps the user read and update their codebase in a conversational loop.
Always:
- Refresh the context by dumping entire codebase and recent git history.
- Respect .gitignore via Git.
- Emit PowerShell commands in a script block.
- Provide a one-line commit message at the top."""

def detect_os():
    return platform.system()

def gather_codebase(root: Path) -> str:
    proc = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=str(root), capture_output=True, text=True, check=True
    )
    dump = []
    for rel in proc.stdout.splitlines():
        path = root / rel
        if path.is_file() and path.suffix.lower() in {'.py', '.md', '.txt', '.json'}:
            dump.append(f"# File: {rel}\n" + path.read_text(encoding='utf-8'))
    return "\n\n".join(dump)

def write_context(root: Path):
    ctx = gather_codebase(root)
    log = subprocess.run(
        ["git", "log", "--oneline", "-n", "20"],
        cwd=str(root), capture_output=True, text=True, check=True
    ).stdout
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"OS: {detect_os()}\n\n=== CODEBASE ===\n{ctx}\n\n=== GIT LOG ===\n{log}")

def send_message(msg: str) -> str:
    write_context(Path.cwd())
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":msg}
        ]
    )
    return resp.choices[0].message.content

def extract_and_save(script: str) -> bool:
    if '```powershell' not in script: return False
    ps = script.split('```powershell')[1].split('```')[0].strip()
    with open(UPDATE_SCRIPT, 'w', encoding='utf-8') as f:
        f.write(ps)
    print(f"[+] Wrote {UPDATE_SCRIPT}")
    return True

def main():
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: set OPENAI_API_KEY"); return
    print("Simpler Codex CLI (type 'exit' to quit)")
    while True:
        msg = input("â€º ").strip()
        if msg.lower() in ("exit","quit"): break
        out = send_message(msg)
        print("\n" + out + "\n")
        if extract_and_save(out):
            print("Run .\\apply_updates.ps1 to apply changes.\n")

if __name__=="__main__":
    main()
