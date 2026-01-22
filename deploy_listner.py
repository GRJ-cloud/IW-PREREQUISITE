from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

CONTAINER_NAME = "hello-python-app"

@app.route("/", methods=['POST'])
def deploy():
    data = request.get_json()
    image = data.get("image")
    tag = data.get("tag", "latest")
    full_image = f"{image}:{tag}"

    # READ SECRETS FROM EC2 HOST ENVIRONMENT
    pat = os.getenv("GITHUB_PAT")
    owner = os.getenv("REPO_OWNER")
    repo = os.getenv("REPO_NAME")

    # Only check for image/tag here since secrets are local
    if not image:
        return {"status": "error", "message": "No image provided"}, 400

    try:
        print(f"📦 Pulling {full_image}...")
        subprocess.run(["docker", "pull", full_image], check=True)

        # FIX FOR PORT ALREADY ALLOCATED:
        # We forcefully remove the container by name.
        # -f stops it if it's running and removes it.
        print("🗑️ Cleaning up old container...")
        subprocess.run(["docker", "rm", "-f", CONTAINER_NAME], stderr=subprocess.DEVNULL)

        # Start new container injecting local host secrets
        print("🚀 Starting new container...")
        subprocess.run([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", "8000:8000",
            "-e", f"GITHUB_PAT={pat}",
            "-e", f"REPO_OWNER={owner}",
            "-e", f"REPO_NAME={repo}",
            full_image
        ], check=True)

        return {"status": "success", "message": f"Deployed {tag}"}, 200

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    # Check if variables are set before starting the server
    if not os.getenv("GITHUB_PAT"):
        print("⚠️ WARNING: GITHUB_PAT not found in environment!")
   
    app.run(host="0.0.0.0", port=10010)
