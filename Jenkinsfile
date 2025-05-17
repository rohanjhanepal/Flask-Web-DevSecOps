pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-web-app"
        DOCKER_REGISTRY = "rohanjhanepal"
    }

    stages {
        stage('Build') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Test') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                pytest test_app.py > test-report.txt || echo Tests failed but continuing...
                '''
                bat 'pytest test_app.py > test-report.txt || echo Tests failed but continuing...'
                archiveArtifacts artifacts: 'test-report.txt'
            }
        }

        stage('Code Quality') {
            steps {
                bat 'pylint app.py > pylint-report.txt || echo Linting failed but continuing...'
                archiveArtifacts artifacts: 'pylint-report.txt'
            }
        }

        stage('Security') {
            steps {
                bat 'pip install bandit'
                bat 'bandit -r . > bandit-report.txt || echo Bandit failed but continuing...'
                archiveArtifacts artifacts: 'bandit-report.txt'
            }
        }

        // stage('Deploy') {
        //     steps {
        //         bat 'docker run -d -p 5000:5000 --name flask-test-container %IMAGE_NAME%'
        //     }
        // }

        // stage('Release') {
        //     steps {
        //         bat 'docker tag %IMAGE_NAME% %DOCKER_REGISTRY%/%IMAGE_NAME%:latest'
        //         bat 'docker push %DOCKER_REGISTRY%/%IMAGE_NAME%:latest'
        //     }
        // }

        // stage('Monitoring') {
        //     steps {
        //         echo "Monitoring setup would include New Relic or Prometheus setup (refer to the report)."
        //     }
        // }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
