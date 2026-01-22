pipeline {
    agent any

    environment {
        // Only non-sensitive config here
        DOCKER_IMAGE   = "gj5998/hello-python-app"
        EC2_IP         = "${env.EC2_PUBLIC_IP}"
    }

    stages {
        stage('Prepare') {
            steps {
                script {
                    env.GIT_COMMIT_ID = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                }
            }
        }

        stage('Build & Push') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-password', variable: 'DOCKER_PASS')]) {
                    sh """
                        docker build -t ${DOCKER_IMAGE}:${GIT_COMMIT_ID} -t ${DOCKER_IMAGE}:latest .
                        echo \$DOCKER_PASS | docker login -u gj5998 --password-stdin
                        docker push ${DOCKER_IMAGE}:${GIT_COMMIT_ID}
                        docker push ${DOCKER_IMAGE}:latest
                    """
                }
            }
        }

        stage('Trigger Deployment') {
            steps {
                // Simplified payload: No secrets sent over the network
                sh """
                    curl -X POST http://${EC2_IP}:10010 \
                    -H "Content-Type: application/json" \
                    -d '{"image": "${DOCKER_IMAGE}", "tag": "${GIT_COMMIT_ID}"}'
                """
            }
        }
    }
}
