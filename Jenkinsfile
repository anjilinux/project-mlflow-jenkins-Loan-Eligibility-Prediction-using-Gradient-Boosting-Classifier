pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "Loan_Eligibility_GBC"
    }

    stages {

        /* ================================
           Stage 1: Checkout
        ================================= */
        stage("Checkout Code") {
            steps {
                git branch: "master",
                    url: "https://github.com/anjilinux/project-mlflow-jenkins-Loan-Eligibility-Prediction-using-Gradient-Boosting-Classifier.git"
            }
        }

        /* ================================
           Stage 2: Setup Virtual Environment
        ================================= */
        stage("Setup Virtual Environment") {
            steps {
                sh '''
                python3 -m venv $VENV_NAME
                . $VENV_NAME/bin/activate
              
                pip install -r requirements.txt
                '''
            }
        }

        /* ================================
           Stage 3: Data Ingestion
        ================================= */
        stage("Data Ingestion") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python data_ingestion.py
                '''
            }
        }

        /* ================================
           Stage 4: EDA & Feature Engineering
        ================================= */
        stage("EDA & Feature Engineering") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python feature_engineering.py
                '''
            }
        }

        /* ================================
           Stage 5: Data Preprocessing
        ================================= */
        stage("Data Preprocessing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python preprocess.py
                '''
            }
        }

        /* ================================
           Stage 6: Model Training
        ================================= */
        stage("Model Training") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python train.py
                '''
            }
        }

        /* ================================
           Stage 7: Model Evaluation
        ================================= */
        stage("Model Evaluation") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python evaluate.py
                '''
            }
        }

        /* ================================
           Stage 8: Pytest - Data
        ================================= */
        stage("Pytest - Data") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                export PYTHONPATH=$(pwd)
                pytest test_data.py
                '''
            }
        }

        /* ================================
           Stage 9: Pytest - Model
        ================================= */
        stage("Pytest - Model") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                export PYTHONPATH=$(pwd)
                pytest test_model.py
                '''
            }
        }



        stage("Schema Test1") {
    steps {
        sh '''
        . $VENV_NAME/bin/activate
        pytest test_schema.py
        '''
    }
}


        /* ================================
           Stage 11: Prediction Smoke Test (FastAPI)
        ================================= */
  

  stage("Prediction Test") {
    steps {
        sh '''
        set -e
        . $VENV_NAME/bin/activate
        export PYTHONPATH=$(pwd)

        echo "Starting FastAPI..."
        nohup uvicorn main:app --host 0.0.0.0 --port 8005 > uvicorn.log 2>&1 &
        API_PID=$!
        echo "FastAPI PID: $API_PID"
        trap "kill $API_PID 2>/dev/null || true" EXIT

        # Wait loop (up to 30s)
        for i in {1..30}; do
            if curl -s http://localhost:8005/health | grep -q "ok"; then
                echo "✅ FastAPI is running"
                break
            fi
            echo "Waiting for FastAPI... ($i/30)"
            sleep 1
        done

        # Fail if still not ready
        if ! curl -s http://localhost:8005/health | grep -q "ok"; then
            echo "❌ FastAPI failed to start"
            cat uvicorn.log
            exit 1
        fi

        # Prediction test
        RESPONSE=$(curl -s -X POST http://localhost:8005/predict \
            -H "Content-Type: application/json" \
            -d '{
                "Gender": "Male",
                "Married": "Yes",
                "Dependents": "0",
                "Education": "Graduate",
                "Self_Employed": "No",
                "ApplicantIncome": 5000,
                "CoapplicantIncome": 2000,
                "LoanAmount": 150,
                "Loan_Amount_Term": 360,
                "Credit_History": 1,
                "Property_Area": "Urban"
            }')

        echo "API Response: $RESPONSE"

        if [ -z "$RESPONSE" ]; then
            echo "❌ Empty API response"
            exit 1
        fi
        '''
   }
}




















        /* ================================
           Stage 12: Docker Build & Run
        ================================= */
        stage("Docker Build & Run") {
            steps {
                sh '''
                set -e

                # Build Docker image
                docker build -t loan-eligibility .

                # Remove old container if exists
                docker rm -f loan-eligibility || true

                # Pick a random free host port between 8000-8999
                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo "🚀 Running API on host port $HOST_PORT"

                # Run container mapping host port to container port 8005
                CONTAINER_ID=$(docker run -d -p $HOST_PORT:8005 --name loan-eligibility loan-eligibility)

                # Save HOST_PORT and CONTAINER_ID to temporary files for next stage
                echo $HOST_PORT > .docker_host_port
                echo $CONTAINER_ID > .docker_container_id
                '''
            }
        }

        /* ================================
           Stage 13: FastAPI Docker Test
        ================================= */
    stage("FastAPI Docker Test") {
    steps {
        sh '''
        set -e
        HOST_PORT=$(cat .docker_host_port)
        CONTAINER_ID=$(cat .docker_container_id)

        # Wait for container health
        for i in {1..30}; do
            curl -sSf http://localhost:$HOST_PORT/health && break
            echo "Waiting for Docker FastAPI..."
            sleep 1
        done

        RESPONSE=$(curl -s -X POST http://localhost:$HOST_PORT/predict \
            -H "Content-Type: application/json" \
            -d '{
                "Gender": "Male",
                "Married": "Yes",
                "Dependents": "0",
                "Education": "Graduate",
                "Self_Employed": "No",
                "ApplicantIncome": 5000,
                "CoapplicantIncome": 2000,
                "LoanAmount": 150,
                "Loan_Amount_Term": 360,
                "Credit_History": 1,
                "Property_Area": "Urban"
            }')

        echo "Docker API Response: $RESPONSE"
        '''
   }  

 }


        /* ================================
           Stage 14: Archive Artifacts
        ================================= */
        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: 'artifacts/*.pkl', fingerprint: true
            }
        }
    }



    post {
        success {
            echo "✅ Loan Eligibility MLOps Pipeline Completed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Logs"
        }
    }
}

 


