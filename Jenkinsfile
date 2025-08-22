pipeline{
    agent any

    tools {
        git 'Default'
        dockerTool 'docker-latest'
    }

    environment {
        REPO_URL = 'https://github.com/SZGYuval/GitOps-CI-New.git'
        DOCKER_REPO = 'szgyuval123/gitops-repo'
    }

    stages{
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Early exit on [skip ci]') {
            steps {
                script {
                    def msg = sh(returnStdout: true, script: "git log -1 --pretty=%B").trim()
                    if (msg.toLowerCase().contains('[skip ci]')) {
                        echo 'Found [skip ci]; skipping remaining stages.'
                        env.SKIP_CI = 'true'
                    }
                }
            }
        }

        stage("Verify git version"){
            when {
                beforeAgent true
                not { environment name: 'SKIP_CI', value: 'true' }
            }

            steps{
                sh 'git --version'
                sh 'docker --version'
            }
        }

        stage("Tag Image") {
            when {
                beforeAgent true
                not { environment name: 'SKIP_CI', value: 'true' }
            }

            steps {
                sh '''
                    set -euo pipefail

                    CUR="$(cat VERSION | tr -d '\r\n')"
                    MAJOR=$(echo "$CUR" | cut -d. -f1)
                    MINOR=$(echo "$CUR" | cut -d. -f2)
                    PATCH=$(echo "$CUR" | cut -d. -f3)

                    LOG="$(git log -1 --no-merges --pretty=%B | tr -d '\r')"

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
                '''
            }
        }

        stage("Push changes to git repository") {
            when {
                beforeAgent true
                not { environment name: 'SKIP_CI', value: 'true' }
            }

            steps {
                withCredentials([string(credentialsId: 'github-creds', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        set -euo pipefail
                        git config user.name  "jenkins"
                        git config user.email "jenkins@local"

                        if git diff --quiet -- VERSION; then
                           echo "VERSION unchanged; skipping push"
                           exit 0
                        fi

                        git add VERSION
                        git commit -m "new image version [skip ci]"

                        PUSH_URL="https://${GITHUB_TOKEN}@${REPO_URL#https://}"
                        git push "$PUSH_URL" "HEAD:main"
                    '''
                }
            }
        }

        stage("Building Docker image") {
            when {
                beforeAgent true
                not { environment name: 'SKIP_CI', value: 'true' }
            }

            steps { 
                sh '''
                    set -euo pipefail
                    TAG="$(tr -d '\\r\\n' < VERSION)"
                    IMAGE=$DOCKER_REPO
                    echo "Building ${IMAGE}:${TAG}"
                    docker build -t "${IMAGE}:${TAG}" .
                '''      
            }
        }

        stage("Unit Tests") {
            when {
                beforeAgent true
                not {environment name: 'SKIP_CI', value: 'true'}
            }

            steps {
                sh 'echo add unit tests!!'
            }
        }

        stage ('Push Image') {
            when {
                beforeAgent true
                not {environment name: 'SKIP_CI', value: 'true'}
            }

            steps {
                withDockerRegistry(credentialsId: 'docker-hub-creds', url: "") {
                    sh '''
                        set -eu
                        TAG="$(tr -d '\\r\\n' < VERSION)"
                        echo "Pushing ${DOCKER_REPO}:${TAG}"
                        docker push "${DOCKER_REPO}:${TAG}"
                    '''
                } 
            }
        }

        stage ('Cloning Repository') {
            when {
                beforeAgent true
                not {environment name: 'SKIP_CI', value: 'true'}
            }

            steps {
                dir('gitops-cd') {
                    git branch: 'main', changelog: false, poll: false, url: 'https://github.com/SZGYuval/GitOps-CD'
                }
            }
        }

        stage ('replacing deployment manifest image and push to CD repository') {
            when {
                beforeAgent true
                not {environment name: 'SKIP_CI', value: 'true'}
            }

            steps {
                script {
                    env.TAG = sh(returnStdout: true, script: "tr -d '\\r\\n' < VERSION").trim()
                }
                withCredentials([string(credentialsId: 'github-creds', variable: 'GITHUB_TOKEN')]) {
                    dir('gitops-cd') {
                        sh ''' 
                            sed -i "s|image: .*|image: ${DOCKER_REPO}:${TAG}|" deployment.yaml

                            git config user.name "jenkins"
                            git config user.email "jenkins@local"

                            if git diff --quiet -- "deployment.yaml"; then
                                echo "No image change detected; skipping push"
                                exit 0
                            fi

                            git add deployment.yaml
                            git commit -m "update deployment manifest"

                            REMOTE="$(git config --get remote.origin.url)"
                            PUSH_URL="https://${GITHUB_TOKEN}@${REMOTE#https://}"
                            git push "$PUSH_URL" "HEAD:main"
                        ''' 
                    }                   
                }
            }
        }
    }

}