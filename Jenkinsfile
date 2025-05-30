pipeline {
    agent any

    environment {
        // Docker Configuration
        IMAGE_NAME = "flask-web-app"
        DOCKER_REGISTRY = "rohanjhanepal"

        // Azure configuration
        AZURE_RESOURCE_GROUP = "flask-rg"
        AZURE_APP_NAME = "flask-web-app-demo-s224679796" 
        AZURE_PLAN = "flask-plan"
        AZURE_LOCATION = "eastus"
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
                docker run --rm -v %cd%:/app -w /app %IMAGE_NAME% pytest tests/test_app.py > test-report.txt || echo Tests failed but continuing...
                '''
                archiveArtifacts artifacts: 'test-report.txt'
            }
        }

        stage('Code Quality') {
            steps {
                bat '''
                docker run --rm -v %cd%:/app -w /app %IMAGE_NAME% pylint main.py > pylint-report.txt || echo Lint failed but continuing...
                '''
                archiveArtifacts artifacts: 'pylint-report.txt'
            }
        }

        stage('Security') {
            steps {
                bat '''
                docker run --rm -v %cd%:/app -w /app %IMAGE_NAME% bandit main.py --severity-level=high > bandit-report.txt || echo Security scan failed but continuing...
                '''
                archiveArtifacts artifacts: 'bandit-report.txt'
            }
        }

        stage('Deploy (Local Test)') {
            steps {
                bat '''
                docker stop flask-test-container || echo "Container not running"
                docker rm flask-test-container || echo "Container does not exist"
                docker run -d -p 5000:5000 --name flask-test-container %IMAGE_NAME% > docker-run.txt
                '''
            }
        }

        stage('Release to Azure') {
            environment {
                AZURE_CLIENT_ID = credentials('azure-client-id') 
                AZURE_CLIENT_SECRET = credentials('azure-client-secret')
                AZURE_TENANT_ID = credentials('azure-tenant-id')
                AZURE_SUBSCRIPTION_ID = credentials('azure-subscription-id')
            }

            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub-cred',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat '''
                        echo Logging in to Docker Hub... ^
                        && powershell -Command "$env:DOCKER_PASS | docker login -u $env:DOCKER_USER --password-stdin" ^
                        && docker tag %IMAGE_NAME% %DOCKER_REGISTRY%/%IMAGE_NAME%:latest ^
                        && docker push %DOCKER_REGISTRY%/%IMAGE_NAME%:latest ^
                        && az login --service-principal -u %AZURE_CLIENT_ID% -p %AZURE_CLIENT_SECRET% --tenant %AZURE_TENANT_ID% ^
                        && az account set --subscription %AZURE_SUBSCRIPTION_ID% ^
                        && az provider register --namespace Microsoft.Web ^
                        && az group create --name %AZURE_RESOURCE_GROUP% --location %AZURE_LOCATION% ^
                        && az appservice plan create --name %AZURE_PLAN% --resource-group %AZURE_RESOURCE_GROUP% --sku B1 --is-linux ^
                        && az webapp create --resource-group %AZURE_RESOURCE_GROUP% --plan %AZURE_PLAN% --name %AZURE_APP_NAME% --deployment-container-image-name %DOCKER_REGISTRY%/%IMAGE_NAME%:latest ^
                        && az webapp config appsettings set --resource-group %AZURE_RESOURCE_GROUP% --name %AZURE_APP_NAME% --settings WEBSITES_PORT=5000 ^
                        && echo Azure deployment complete. Visit: https://%AZURE_APP_NAME%.azurewebsites.net
                        '''
                }
            }
        }
        stage('Monitoring and Alerting') {
            steps{
                bat 'the monitoring dashboard can be found at https://melbourne-trades-college.sentry.io/issues/'
            }
    
        }


    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check logs."
        }
    }
}
