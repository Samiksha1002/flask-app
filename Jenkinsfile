pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "3.110.133.193"       /*public-ip*/
        IMAGE_NAME = "sam1002/flask-cicd:latest"
        APP_NAME = "flask-cicd-app"
        APP_PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/<your-username>/flask-cicd-app.git'
            }
        }

        stage('Test') {
            steps {
                sh 'pip3 install -r requirements.txt && pytest'
            }
        }

        stage('Build & Push Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME .
                docker push $IMAGE_NAME
                '''
            }
        }

        stage('Deploy on AWS EC2') {
            steps {
                sh '''
                ssh $EC2_USER@$EC2_HOST "
                  docker pull $IMAGE_NAME &&
                  docker stop $APP_NAME || true &&
                  docker rm $APP_NAME || true &&
                  docker run -d \
                    --name $APP_NAME \
                    -p $APP_PORT:$APP_PORT \
                    $IMAGE_NAME
                "
                '''
            }
        }
    }
}
