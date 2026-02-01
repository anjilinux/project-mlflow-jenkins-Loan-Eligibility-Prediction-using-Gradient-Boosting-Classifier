pipeline {
    agent any

    environment {
        VENV_NAME = "venv"
        MLFLOW_TRACKING_URI = "http://localhost:5555"
        MLFLOW_EXPERIMENT_NAME = "Loan_Eligibility_GBC"
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
stage("test_data") {
    steps {
        sh '''
        . $VENV_NAME/bin/activate
        export PYTHONPATH=$WORKSPACE
        pytest
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
        export PYTHONPATH=$WORKSPACE
        pytest
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
curl -s -X POST http://localhost:7000/predict \
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
}'


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
   
       /* ================================
   Stage 11: Docker Build & Test
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

        # Run container mapping random host port to container port 8005
        CONTAINER_ID=$(docker run -d -p $HOST_PORT:8005 --name loan-eligibility loan-eligibility)

        # Wait for the API to start
        sleep 10

        # Health check
        curl -sf http://localhost:$HOST_PORT/health || {
            echo "❌ API health check failed"
            docker logs $CONTAINER_ID
            exit 1
        }

        # Test prediction endpoint with all required fields
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
