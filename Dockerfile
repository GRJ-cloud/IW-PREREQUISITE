FROM python:3.9-slim

WORKDIR /app

# Arguments from Jenkins
ARG GITHUB_PAT
ARG REPO_OWNER
ARG REPO_NAME

# Environment setup
ENV GITHUB_PAT=$GITHUB_PAT \
    REPO_OWNER=$REPO_OWNER \
    REPO_NAME=$REPO_NAME \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv

# Explicitly use python3 to create the venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

# Use python3 -m pip for the most reliable installation
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Final execution using python3
CMD ["python3", "app.py"]
