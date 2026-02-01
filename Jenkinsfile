pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "Loan_Eligibility_GBC"
        APP_PORT = "8005"
    }

    options {
        timeout(time: 60, unit: 'MINUTES')
        ansiColor('xterm')
    }

    stages {

        /* ================================
           Stage 1: Checkout Code
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
           Stage 8: Pytest - Data & Model
        ================================= */
        stage("Run Pytests") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                export PYTHONPATH=$(pwd)
                pytest test_data.py
                pytest test_model.py
                pytest test_schema.py
                '''
            }
        }

        /* ================================
           Stage 9: FastAPI Local Smoke Test
        ================================= */
        stage("FastAPI Prediction Test") {
            steps {
                sh '''
                set -e
                . $VENV_NAME/bin/activate
                export PYTHONPATH=$(pwd)

                echo "Starting FastAPI..."
                nohup uvicorn main:app --host 0.0.0.0 --port $APP_PORT > uvicorn.log 2>&1 &
                API_PID=$!
                echo "FastAPI PID: $API_PID"
                trap "kill $API_PID 2>/dev/null || true" EXIT

                # Wait until FastAPI /health is ready
                for i in {1..30}; do
                    if curl -s http://localhost:$APP_PORT/health | grep -q "ok"; then
                        echo "✅ FastAPI is running"
                        break
                    fi
                    echo "Waiting for FastAPI... ($i/30)"
                    sleep 1
                done

                # Fail if still not ready
                if ! curl -s http://localhost:$APP_PORT/health | grep -q "ok"; then
                    echo "❌ FastAPI failed to start"
                    cat uvicorn.log
                    exit 1
                fi

                # Prediction test
                RESPONSE=$(curl -s -X POST http://localhost:$APP_PORT/predict \
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

                kill $API_PID
                '''
            }
        }

        /* ================================
           Stage 10: Docker Build & Run
        ================================= */
        stage("Docker Build & Run") {
            steps {
                sh '''
                set -e
                docker build -t loan-eligibility .
                docker rm -f loan-eligibility || true

                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo "🚀 Running API on host port $HOST_PORT"

                CONTAINER_ID=$(docker run -d -p $HOST_PORT:$APP_PORT --name loan-eligibility loan-eligibility)
                echo $HOST_PORT > .docker_host_port
                echo $CONTAINER_ID > .docker_container_id
                '''
            }
        }

        /* ================================
           Stage 11: FastAPI Docker Test
        ================================= */
        stage("FastAPI Docker Test") {
            steps {
                sh '''
                set -e
                HOST_PORT=$(cat .docker_host_port)
                CONTAINER_ID=$(cat .docker_container_id)

                echo "Waiting for Docker FastAPI..."
                for i in {1..30}; do
                    if curl -sSf http://localhost:$HOST_PORT/health > /dev/null; then
                        echo "✅ Docker FastAPI is ready"
                        break
                    fi
                    echo "⏳ Waiting... ($i/30)"
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

                # Stop & remove container
                docker stop $CONTAINER_ID
                docker rm $CONTAINER_ID
                rm -f .docker_host_port .docker_container_id
                '''
            }
        }

        /* ================================
           Stage 12: Archive Artifacts
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
