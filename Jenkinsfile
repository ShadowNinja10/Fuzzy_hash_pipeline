pipeline {
  agent any

  environment {
    PYTHONUNBUFFERED = '1'
    MONGO_URI        = 'mongodb://127.0.0.1:27017'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python Environment') {
      steps {
        sh 'source ~/venvs/datasci/bin/activate'
      }
    }

    stage('1) Retrieve Hashes') {
      steps {
        sh 'chmod +x scripts/retrieve_hashes.py'
        sh 'python3 scripts/retrieve_hashes.py'
        archiveArtifacts artifacts: 'hashes.json', fingerprint: true
      }
    }

    stage('2) Init MongoDB') {
      steps {
        sh 'chmod +x scripts/init_mongodb.py'
        sh 'python3 scripts/init_mongodb.py'
      }
    }

    stage('3) Process & Store') {
      steps {
        sh 'chmod +x scripts/process_hashes.py'
        sh 'python3 scripts/process_hashes.py'
      }
    }
  }

  post {
    success {
      echo "✅ Done! Unique vs. duplicates are in MongoDB."
    }
    failure {
      echo "❌ Something went wrong. Check the logs."
    }
  }
}
