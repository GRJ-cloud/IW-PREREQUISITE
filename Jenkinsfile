pipeline {
    agent any

    environment {
        // Pulling from Jenkins Global Properties (Manage Jenkins > System)
        DOCKER_IMAGE   = "gj5998/hello-python-app"
        EC2_IP         = "${env.EC2_PUBLIC_IP}"
        OWNER          = "${env.REPO_OWNER}"
        REPO           = "${env.REPO_NAME}"
    }

    stages {
        stage('Prepare') {
            steps {
                script {
                    // Extract Short SHA
                    env.GIT_COMMIT_ID = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
            }
        }

        stage('Build & Inject Secrets') {
            steps {
                // We pull the GitHub PAT securely just for the build process
                withCredentials([string(credentialsId: 'github-pat', variable: 'PAT')]) {
                    sh """
                        docker build \
                        --build-arg GITHUB_PAT=${PAT} \
                        --build-arg REPO_OWNER=${OWNER} \
                        --build-arg REPO_NAME=${REPO} \
                        -t ${DOCKER_IMAGE}:${GIT_COMMIT_ID} \
                        -t ${DOCKER_IMAGE}:latest .
                    """
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-password', variable: 'DOCKER_PASS')]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u gj5998 --password-stdin
                        docker push ${DOCKER_IMAGE}:${GIT_COMMIT_ID}
                        docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Trigger Deployment') {
            steps {
                // Using the IP we fetched from Global Properties
                sh """
                    curl -X POST http://${EC2_IP}:10010 \
                    -H "Content-Type: application/json" \
                    -d '{"image": "${DOCKER_IMAGE}", "tag": "${GIT_COMMIT_ID}"}'
                """
            }
        }
    }
}
