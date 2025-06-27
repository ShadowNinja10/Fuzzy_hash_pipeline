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
      // steps {
      //   // sh 'source ~/venvs/datasci/bin/activate'
      //   sh '''
      //     source /Users/jayesh.chaudhari@cohesity.com/venvs/datasci/bin/activate
      //     pip install --upgrade pip
      //     pip install virustotal-cli ppdeep pymongo
      //   '''
      // }

      steps {
        sh '''
          # install vt via brew if it's not already present
          if ! command -v vt >/dev/null 2>&1; then
            echo "Installing vt CLI via Homebrew…"
            brew update
            brew install virustotal-cli
          fi

          # make sure pip deps are there
          pip install --upgrade ppdeep pymongo
        '''
      }
    }

    // stage('1) Retrieve Hashes') {
    //   steps {
    //     sh 'chmod +x scripts/retrieve_hashes.py'
    //     sh 'python3 scripts/retrieve_hashes.py'
    //     archiveArtifacts artifacts: 'hashes.json', fingerprint: true
    //   }
    // }

    stage('1) Retrieve Hashes') {
      steps {
        // this injects your secret text into $VT_API_KEY
        withCredentials([string(credentialsId: 'vt-api-key', variable: 'VT_API_KEY')]) {
          sh '''
            # initialize the vt CLI
            vt init $VT_API_KEY
            
            # now your Python script can call `vt search ...`
            chmod +x scripts/retrieve_hashes.py
            python3 scripts/retrieve_hashes.py
          '''
        }
        archiveArtifacts artifacts: 'hashes.json'
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
