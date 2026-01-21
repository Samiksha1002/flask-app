pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "3.110.133.193"       /*public-ip*/
        IMAGE_NAME = "sam1002/flask-cicd"
        APP_NAME = "flask-cicd-app"
        APP_PORT = "5000"
        DOCKERCREDENTIALS = credentials("dockerhub")
    }

    stages {

        /*stage('Checkout') {
            steps {
                git 'https://github.com/Samiksha1002/flask-app.git'
            }
        }*/

        stage('Test') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
        
                pip install --upgrade pip
                pip install -r requirements.txt
        
                pytest
                '''
            }
        }



        stage("Docker Image")
        {
            steps {
                sh """
                    echo "========Building the Docker Image ============"
                    echo "IMAGE Name is - ${IMAGE_NAME}"
                    docker build -t $IMAGE_NAME:"${env.BUILD_NUMBER}" .
                    echo "====== Building Image Completed ====="
                    """      
            }
        }

        stage("Docker Login and push the image")
        {
            steps{
                sh """
                    echo "======== Login the Docker Hub ============"
                        echo "Docker credentials - ${DOCKERCREDENTIALS}"
                        docker login -u $DOCKERCREDENTIALS_USR -p $DOCKERCREDENTIALS_PSW
                        docker push $IMAGE_NAME:"${env.BUILD_NUMBER}"
                    echo "====== Login successful====="
                    """      
                } 
        }

        stage('Deploy on AWS EC2') {
            steps {
            sshagent(credentials: ['ec2-ssh-key']) {
                sh '''
                ssh -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST "
                  docker pull $IMAGE_NAME$:{env.BUILD_NUMBER} &&
                  docker stop $APP_NAME || true &&
                  docker rm $APP_NAME || true &&
                  docker run -d \
                    --name $APP_NAME \
                    -p $APP_PORT:$APP_PORT \
                    $IMAGE_NAME:${env.BUILD_NUMBER}
                "
                '''
                }
            }
        }
    }
}
