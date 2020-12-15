def build_app(){
  sh 'docker-compose build'
  sh 'docker-compose up -d'
}

def build_env(){
  sh 'python3 -m pip install -r requirements.txt'
}

def test_app(){
  sh 'python3 test_app.py'
}

def down_app(){
  input message: 'Finished using the web site? (Click "Proceed" to continue)'
  sh 'docker-compose down'
}

def release_app(){
  
}

def live_app(){
  echo 'merge into master'
}

return this
