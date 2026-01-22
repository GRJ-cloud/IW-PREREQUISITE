from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

CONTAINER_NAME = "hello-python-app"

@app.route("/", methods=['POST'])
def deploy():
    # 1. Extract everything from the Webhook Payload
    data = request.get_json()
   
    image = data.get("image")
    tag = data.get("tag", "latest")
   
    # Credentials passed from Jenkins
    pat = data.get("github_pat")
    owner = data.get("repo_owner")
    repo = data.get("repo_name")

    # Guard clause
    if not all([image, pat, owner, repo]):
        return {"status": "error", "message": "Incomplete payload from Jenkins"}, 400

    full_image = f"{image}:{tag}"

    try:
        # Step A: Pull
        subprocess.run(["docker", "pull", full_image], check=True)

        # Step B: Stop/Remove
        subprocess.run(["docker", "stop", CONTAINER_NAME], stderr=subprocess.DEVNULL)
        subprocess.run(["docker", "rm", CONTAINER_NAME], stderr=subprocess.DEVNULL)

        # Step C: Run and inject the secrets received from the webhook
        subprocess.run([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", "8000:8000",
            "-e", f"GITHUB_PAT={pat}",
            "-e", f"REPO_OWNER={owner}",
            "-e", f"REPO_NAME={repo}",
            full_image
        ], check=True)

        return {"status": "success", "message": f"Deployed {tag} with injected secrets"}, 200

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10010)
