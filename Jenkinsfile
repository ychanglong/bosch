pipeline {
    agent any

    environment {
        http_proxy = 'http://10.187.215.117:3128'
        https_proxy = 'http://10.187.215.117:3128'
        no_proxy = 'localhost,127.0.0.1,.bosch.com'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ychanglong/bosch.git'
            }
        }
        stage('Build') {
            steps {
                script {
                    sh 'sudo docker-compose -f docker-compose.yml up -d --build'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    sh 'sudo docker-compose -f docker-compose.yml up -d'
                }
            }
        }
    }
}