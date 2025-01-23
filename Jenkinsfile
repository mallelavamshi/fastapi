pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'your-image-name'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DIFY_API_KEY = credentials('dify-api-key')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    // Create .env file
                    sh """
                    cat > .env << EOL
                    DIFY_API_KEY=${DIFY_API_KEY}
                    EOL
                    """
                    
                    // Create SSL directory
                    sh 'mkdir -p nginx/ssl'
                    
                    // Copy SSL certificates
                    sh '''
                    sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/your-cert.pem
                    sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/your-key.pem
                    sudo chown -R jenkins:jenkins nginx/ssl
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    // Add your test commands here
                    sh 'echo "Running tests..."'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    // Stop existing containers
                    sh 'docker-compose down || true'
                    
                    // Start new containers
                    withCredentials([string(credentialsId: 'dify-api-key', variable: 'DIFY_API_KEY')]) {
                        sh 'docker-compose up -d'
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up old images
            sh 'docker system prune -f'
            
            // Clean workspace
            cleanWs()
        }
    }
}