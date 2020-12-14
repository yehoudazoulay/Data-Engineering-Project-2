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
        sh 'docker-compose up -d'
      }
    }
   
    stage('Testing'){
      steps{
	sh 'python3 -m pip install -r requirements.txt'
        sh 'python3 test_app.py'
      }
    }
    stage('Docker shutdown'){
      steps{
	
        sh 'docker-compose down'
      }
    }
  }
}
