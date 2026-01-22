FROM python:3.9-slim

WORKDIR /app


ARG GITHUB_PAT
ARG REPO_OWNER
ARG REPO_NAME


ENV GITHUB_PAT=$GITHUB_PAT
ENV REPO_OWNER=$REPO_OWNER
ENV REPO_NAME=$REPO_NAME

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python3", "app.py"]
