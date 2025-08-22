pipeline{
    agent any

    tools {
        git 'Default'
        dockerTool 'docker-latest'
    }

    stages{
        stage("Verify git version"){
            steps{
                sh 'git --version'
                sh 'docker --version'
            }
        }
    }

}