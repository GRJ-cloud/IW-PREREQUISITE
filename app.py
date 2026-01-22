import os
import requests
from flask import Flask

app = Flask(__name__)

# --- CONFIGURATION FROM ENV VARS ---
# Make sure these are set in your environment
GITHUB_PAT = os.getenv("GITHUB_PAT")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_NAME = os.getenv("REPO_NAME")

def get_latest_github_commit():
    """Fetches the latest commit ID and message from GitHub API."""
    if not all([GITHUB_PAT, REPO_OWNER, REPO_NAME]):
        return "Missing Config", "Ensure GITHUB_PAT, REPO_OWNER, and REPO_NAME are set."

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/commits"
    headers = {
        "Authorization": f"Bearer {GITHUB_PAT}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        # per_page=1 ensures we only get the very latest commit
        response = requests.get(url, headers=headers, params={"per_page": 1})
        response.raise_for_status()
       
        data = response.json()[0]
        commit_id = data['sha']
        commit_message = data['commit']['message']
       
        return commit_id, commit_message

    except Exception as e:
        return "Error", f"Could not fetch commit: {str(e)}"

@app.route("/")
def home():
    # Fetch both pieces of info in one go
    commit_id, commit_message = get_latest_github_commit()

    return f"""
    <h1>Hello World</h1>
    <p><strong>Latest Git Commit ID:</strong> {commit_id}</p>
    <p><strong>Latest Git Commit Message:</strong> {commit_message}</p>
    <p><small>Source: GitHub API (Remote)</small></p>
    """

if __name__ == "__main__":
    # You can also use host="0.0.0.0" for Docker/External access
    app.run(host="0.0.0.0", port=8000, debug=True)
