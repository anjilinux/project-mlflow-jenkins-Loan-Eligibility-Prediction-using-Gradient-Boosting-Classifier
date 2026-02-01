#!/bin/bash


 #    mlflow with jenkins - pipeline , virtual environment python, Data Collection, Exploratory Data Analysis ,Feature Engineering, Data Preparation & Preprocessing,Model Training ,Model Evaluation,artifacts,pytest model, testing model,Model Deployment flask fastapi,ddockerfile docker image Monitoring






# Create directories
mkdir  $FILES

# Define files
FILES=(
lean_data.csv
logger.py
requirements.txt
feature_engineering.py
data_ingestion.py
data_preprocessing.py
train.py
evaluate.py
predict.py
test_model.py
main.py
app.py
Dockerfile
Jenkinsfile
test_data.py
schema.py



)

# Create files
for FILE_NAME in "${FILES[@]}"; do
    touch "$FILE_NAME"
    echo "Created file: $FILE_NAME"
done

echo "✅ All specified files have been created."
