pipeline{
  agent any
  stages {
    stage('Build Flask app'){
      steps{
        sh 'docker-compose build'
      }
    }
    
    stage('Run Flask app'){
      steps{
        sh 'docker-compose up'
      }
    }
   
    stage('Testing'){
      steps{
        sh 'python test_app.py'
      }
    }
    stage('Docker shutdown'){
      steps{
        sh 'docker-compose down'
      }
    }
  }
}
