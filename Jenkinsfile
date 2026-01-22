pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gj5998/hello-python-app"
    }

    stages {

        stage('Prepare') {
            steps {
                script {
                    def gitCommitId = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                    env.GIT_COMMIT_ID = gitCommitId
                }
            }
        }

        stage('Build Docker Image') {
            steps {
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

        stage('Trigger Webhook') {
            steps {
                sh """
                  curl -X POST http://localhost:10010 \
                  -H "Content-Type: application/json" \
                  -d '{"image":"${DOCKER_IMAGE}","tag":"latest"}'
                """
            }
        }
    }
}
