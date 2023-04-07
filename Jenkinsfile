pipeline {
    agent {
        kubernetes {
            label 'docker'
        }
    }
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        IMAGE = "jestenok/jira-telegram-bot"
        VERSION = "1.1"
        TAG = "${IMAGE}:${VERSION}.${BUILD_NUMBER}"
    }
    stages {
        stage('Git clone') {
            steps {
                script {
                    container('docker') {
                        git 'https://github.com/jestenok/jira-telegram-bot'
                    }
                }
            }
        }
        stage('Build') {
            steps {
                container('docker') {
                    sh 'docker build -t $TAG .'
                }
            }
        }
        stage('Login') {
            steps {
                container('docker') {
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                }
            }
        }
        stage('Push') {
            steps {
                container('docker') {
                    sh 'docker push $TAG'
                }
            }
        }
    }
    post {
        always {
            container('docker') {
                sh 'docker logout'
            }
        }
    }
}