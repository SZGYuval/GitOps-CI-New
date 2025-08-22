pipeline{
    agent any

    tools {
        git 'Default'
        dockerTool 'docker-latest'
    }

    stages{
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage("Verify git version"){
            steps{
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage("build image") {
            steps {
                sh(script: '''
                    set -euo pipefail

                    CUR="$(cat VERSION | tr -d '\r\n')"
                    MAJOR=$(echo "$CUR" | cut -d. -f1)
                    MINOR=$(echo "$CUR" | cut -d. -f2)
                    PATCH=$(echo "$CUR" | cut -d. -f3)
                    
                    LOG="$(git log -1 --pretty=%B | tr -d '\\r')"
                    shopt -s nocasematch
                    if [[ "$LOG" == *major* ]]; then
                        MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0
                    elif [[ "$LOG" == *minor* ]]; then
                        MINOR=$((MINOR + 1)); PATCH=0 
                    else
                        PATCH=$((PATCH + 1))
                    fi

                    NEXT="${MAJOR}.${MINOR}.${PATCH}"

                    echo "Current: $CUR"
                    echo "Next:    $NEXT"
                    echo "$NEXT" > VERSION
                ''', shell: '/bin/bash')
            }
        }
    }

}