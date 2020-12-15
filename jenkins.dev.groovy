def build_app(){
  sh 'docker-compose up -d'
}

def build_env(){
  sh 'python3 -m pip install -r requirements.txt'
}

def test_app(){
  sh 'python3 test_app.py'
}

def down_app(){
  sh 'docker-compose down'
}

def release_app(){
  echo 'branch into release'
}

def live_app(){
}

return this
