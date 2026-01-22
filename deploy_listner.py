from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

# CONFIGURATION
CONTAINER_NAME = "my-python-app"
PORT_MAPPING = "8000:8000"

@app.route("/", methods=['POST'])
def deploy():
    data = request.get_json()
    image = data.get("image")
    tag = data.get("tag", "latest")
    full_image = f"{image}:{tag}"

    print(f"🚀 Received update request for: {full_image}")

    try:
        # Step 1: Pull the new image
        print("📥 Pulling new image...")
        subprocess.run(["docker", "pull", full_image], check=True)

        # Step 2: Stop and remove the old container (if it exists)
        print("🛑 Stopping old container...")
        subprocess.run(["docker", "stop", CONTAINER_NAME], stderr=subprocess.DEVNULL)
        subprocess.run(["docker", "rm", CONTAINER_NAME], stderr=subprocess.DEVNULL)

        # Step 3: Run the new container
        print("🏃 Starting new container...")
        # Note: We pass the environment variables here if needed
        subprocess.run([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", PORT_MAPPING,
            full_image
        ], check=True)

        return {"status": "success", "message": f"Deployed {full_image}"}, 200

    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10010)
