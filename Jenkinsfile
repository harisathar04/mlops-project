pipeline {
  agent any

  environment {
    DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials') // Add this in Jenkins
    FRONTEND_IMAGE = "harisathar04/flask_frontend"
    BACKEND_IMAGE = "harisathar04/node_backend"
  }

  stages {
    stage('Build Docker Images') {
      steps {
        script {
          sh 'docker compose build'
        }
      }
    }

    stage('Login to Docker Hub') {
      steps {
        sh 'echo "$DOCKER_HUB_CREDENTIALS_PSW" | docker login -u "$DOCKER_HUB_CREDENTIALS_USR" --password-stdin'
      }
    }

    stage('Push Images to Docker Hub') {
      steps {
        sh """
          docker tag mlops-project-frontend $FRONTEND_IMAGE
          docker tag mlops-project-backend $BACKEND_IMAGE
          docker push $FRONTEND_IMAGE
          docker push $BACKEND_IMAGE
        """
      }
    }
  }
}
