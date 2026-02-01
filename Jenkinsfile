pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "Loan Eligibility1"
        API_PORT = "7000"
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
           Stage 2: Virtual Environment
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
           Stage 88: Pytest
        ================================= */
        stage("Model Testing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                pytest test_data.py
                '''
            }
        }

        /* ================================
           Stage 8: Pytest
        ================================= */
        stage("Model Testing") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                pytest test_model.py
                '''
            }
        }

        /* ================================
           Stage 9: Prediction Smoke Test
        ================================= */
        stage("Prediction Test") {
            steps {
                sh '''
                . $VENV_NAME/bin/activate
                python predict.py
                '''
            }
        }


        stage("FastAPI API Test") {
            steps {
                sh '''
                set -e
                . $VENV_NAME/bin/activate

                # Start FastAPI in background
                nohup uvicorn main:app --host 0.0.0.0 --port $API_PORT > api.log 2>&1 &
                API_PID=$!
                sleep 10

                # Check health endpoint, ignore non-zero exit code
                curl -sSf http://localhost:$API_PORT/health || true

                # Call prediction endpoint
                RESPONSE=$(curl -s -X POST http://localhost:$API_PORT/predict \
                -H "Content-Type: application/json" \
                -d '{
                        "area": 1200,
                        "bhk": 2,
                        "bath": 2,
                        "description": "luxury apartment near metro"
                    }') || true

                echo "API Response: $RESPONSE"

                # Stop API
                kill -9 $API_PID || true
                '''
            }
        }


        stage("schema-test-"){
            steps{
                sh '''
                . $ENV_NAME/bin/activate
                    python schema.py
                '''
            }
        }





        /* ================================
           Stage 11: Docker Build & Test
                ================================= */
        stage("Docker Build & Run") {
            steps {
                sh '''
                set -e

                # Build Docker image
                docker build -t real-estate-api1 .

                # Remove old container if exists
                docker rm -f real-estate-api1 || true

                # Pick a random free host port between 8000-8999
                HOST_PORT=$(shuf -i 8000-8999 -n 1)
                echo "🚀 Running API on host port $HOST_PORT"

                # Run container mapping random host port to container port 8005
                CONTAINER_ID=$(docker run -d -p $HOST_PORT:8005 --name real-estate-api1 real-estate-api1)

                # Wait for the API to start
                sleep 10

                # Health check
                curl -sf http://localhost:$HOST_PORT/health || {
                    echo "❌ API health check failed"
                    docker logs $CONTAINER_ID
                    exit 1
                }

                # Optionally, test prediction endpoint
                RESPONSE=$(curl -s -X POST http://localhost:$HOST_PORT/predict \
                -H "Content-Type: application/json" \
                -d '{
                        "area": 1200,
                        "bhk": 2,
                        "bath": 2,
                        "description": "luxury apartment near metro"
                    }') || true

                echo "API Response: $RESPONSE"

                # Stop and remove container after test
                docker stop $CONTAINER_ID
                docker rm $CONTAINER_ID
                '''
            }
        }

         //  #        docker stop $CONTAINER_ID
        //    # docker rm $CONTAINER_ID

        /* ================================
           Stage 12: Archive Artifacts
        ================================= */
        stage("Archive Artifacts") {
            steps {
                archiveArtifacts artifacts: '*.pkl', fingerprint: true
            }
        }
    }


    post {
        success {
            echo "✅ Real Estate Price Prediction MLOps Pipeline Completed Successfully"
        }
        failure {
            echo "❌ Pipeline Failed – Check Logs"
        }
    }
}
