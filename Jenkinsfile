
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gj5998/hello-python-app"
        DOCKER_CREDENTIALS_ID = "docker-userpass"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
                script {
                    GIT_COMMIT_ID = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                docker build -t ${DOCKER_IMAGE}:${GIT_COMMIT_ID} .
                docker tag ${DOCKER_IMAGE}:${GIT_COMMIT_ID} ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${docker-userpass}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    """
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh """
                docker push ${DOCKER_IMAGE}:${GIT_COMMIT_ID}
                docker push ${DOCKER_IMAGE}:latest
                """
            }
        }

        stage('Trigger Webhook') {
            steps {
                sh """
                curl -X POST http://122.176.215.69:10010 \
                -H "Content-Type: application/json" \
                -d '{
                    "image": "${DOCKER_IMAGE}",
                    "tag": "${GIT_COMMIT_ID}"
                }'
                """
            }
        }
    }

    post {
        success {
            echo "Build & Push successful"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
      
