FROM python:3.9-slim

WORKDIR /app

# Optimization: Removed apt-get install git (no longer needed for API calls)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requests flask

COPY . .

# Define ENV placeholders (Optional, acts as documentation)
ENV GITHUB_PAT=""
ENV REPO_OWNER=""
ENV REPO_NAME=""

EXPOSE 8000

CMD ["python3", "app.py"]
