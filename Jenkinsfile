pipeline {
  agent any

  // environment {
  //   PYTHONUNBUFFERED = '1'
  //   MONGO_URI        = 'mongodb://127.0.0.1:27017'
  // }

  environment {
    PYTHONUNBUFFERED = '1'
    MONGO_URI        = 'mongodb://127.0.0.1:27017'

    // Inject your key directly—vt will read this automatically
    VT_API_KEY       = credentials('vt-api-key')
    PATH             = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    // stage('Setup Python Environment') {
    //   steps {
    //     sh 'pip install --upgrade ppdeep pymongo'
    //   }
    // }

    // stage('1) Retrieve Hashes') {
    //   steps {
    //     // this injects your secret text into $VT_API_KEY
    //     withCredentials([string(credentialsId: 'vt-api-key', variable: 'VT_API_KEY')]) {
    //       sh '''
    //         # initialize the vt CLI
    //         vt init $VT_API_KEY
            
    //         # now your Python script can call `vt search ...`
    //         chmod +x scripts/retrieve_hashes.py
    //         python3 scripts/retrieve_hashes.py
    //       '''
    //     }
    //     archiveArtifacts artifacts: 'hashes.json'
    //   }
    // }

    // stage('1) Retrieve Hashes') {
    //   steps {
    //     withCredentials([string(credentialsId: 'vt-api-key', variable: 'VT_API_KEY')]) {
    //       sh '''
    //         # initialize the vt CLI by absolute path
    //         /opt/homebrew/bin/vt init --apikey "$VT_API_KEY" --force
            
    //         # now your Python script can call vt search by absolute path too
    //         chmod +x scripts/retrieve_hashes.py
    //         python3 scripts/retrieve_hashes.py
    //       '''
    //     }
    //     archiveArtifacts artifacts: 'hashes.json'
    //   }
    // }

    stage('1) Retrieve Hashes') {
      steps {
        sh '''
          # No init needed—vt uses VT_API_KEY under the hood
          chmod +x scripts/retrieve_hashes.py
          python3 scripts/retrieve_hashes.py
        '''
      }
      post {
        always { archiveArtifacts artifacts: 'hashes.json', fingerprint: true }
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
