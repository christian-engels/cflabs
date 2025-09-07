import os
import subprocess

def is_codespaces():
    return os.environ.get("CODESPACES") == "true" or "CODESPACE_NAME" in os.environ

if is_codespaces():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Saved from GitHub Codespaces"], check=True)
    subprocess.run(["git", "push"], check=True)
else:
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Saved from local computer"], check=True)
