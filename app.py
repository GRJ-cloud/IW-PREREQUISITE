from flask import Flask
import subprocess

app = Flask(__name__)

def get_git_commit_id():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"]
        ).decode("utf-8").strip()
    except Exception:
        return "Git commit ID not available"

def get_git_commit_message():
    try:
        return subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"]
        ).decode("utf-8").strip()
    except Exception:
        return "Git commit message not available"

@app.route("/")
def home():
    commit_id = get_git_commit_id()
    commit_message = get_git_commit_message()

    return f"""
    <h1>Hello World</h1>
    <p><strong>Latest Git Commit ID:</strong> {commit_id}</p>
    <p><strong>Latest Git Commit Message:</strong> {commit_message}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
