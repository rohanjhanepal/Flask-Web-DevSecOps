pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        SNYK_TOKEN = credentials('snyk-token')
        APP_NAME = "flask-web-app"
        VERSION = "${env.BUILD_ID}"
    }
    stages {
        // Stage 1: Build Docker Image
        stage('Build') {
            steps {
                sh 'docker build -t ${APP_NAME}:${VERSION} .'
            }
        }
        
        // Stage 2: Run Tests
        stage('Test') {
            steps {
                sh 'python -m pytest tests/ --cov=website --junitxml=test-results.xml --cov-report=xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }
        
        // Stage 3: Code Quality (SonarQube)
        stage('Code Quality') {
            steps {
                withSonarQubeEnv('sonarqube-server') {
                    sh 'sonar-scanner -Dsonar.projectKey=flask-web-app -Dsonar.sources=website -Dsonar.python.coverage.reportPaths=coverage.xml'
                }
            }
        }
        
        // Stage 4: Security Scan
        stage('Security') {
            steps {
                sh 'safety check --full-report'
                sh 'snyk test --docker=${APP_NAME}:${VERSION}'
            }
        }
        
        // Stage 5: Deploy to Test
        stage('Deploy to Test') {
            steps {
                sh 'docker-compose -f docker-compose.test.yml up -d'
                sh 'curl --fail http://localhost:5000/health || exit 1'
            }
        }
        
        // Stage 6: Release to Prod (Main Branch Only)
        stage('Release to Prod') {
            when { branch 'main' }
            steps {
                sh 'docker login -u ${DOCKER_HUB_CREDENTIALS_USR} -p ${DOCKER_HUB_CREDENTIALS_PSW}'
                sh 'docker tag ${APP_NAME}:${VERSION} ${APP_NAME}:prod'
                sh 'docker push ${APP_NAME}:prod'
                sh 'docker-compose -f docker-compose.prod.yml up -d'
            }
        }
        
        // Stage 7: Monitoring
        stage('Monitoring') {
            steps {
                sh 'echo "Monitoring configured at http://your-server-ip:3000"'
                // Actual integration would use Prometheus/Grafana here
            }
        }
    }
    post {
        always {
            sh 'docker-compose -f docker-compose.test.yml down || true'
            cleanWs()
        }
    }
}