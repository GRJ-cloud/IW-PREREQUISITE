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

        stage('Build Image') {
            steps {
                // CLEAN BUILD: No secrets are passed here.
                // This makes the image generic and secure.
                sh """
                    docker build \
                    -t ${DOCKER_IMAGE}:${GIT_COMMIT_ID} \
                    -t ${DOCKER_IMAGE}:latest .
                """
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
                // We fetch the secrets here ONLY to send them over the wire to the EC2
                withCredentials([string(credentialsId: 'github-pat', variable: 'PAT')]) {
                    sh """
                        curl -X POST http://${EC2_IP}:10010 \
                        -H "Content-Type: application/json" \
                        -d '{
                            "image": "${DOCKER_IMAGE}",
                            "tag": "${GIT_COMMIT_ID}",
                            "github_pat": "${PAT}",
                            "repo_owner": "${OWNER}",
                            "repo_name": "${REPO}"
                        }'
                    """
                }
            }
        }
    }
}
