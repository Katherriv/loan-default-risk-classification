# Loan Default Risk Prediction API

## Project Overview

This project entails the deployment of an optimized Random Forest classification model through a FastAPI application.

The deployed model includes the following:
- A fitted preprocessing object for imputation of missing values and one-hot encoding
- An optimized Random Forest classification model
- The required raw input feature names
- Lists for numeric and categorical features

The API returns:
- The probability of defaulting on a loan
- The predicted loan default status
- Category of higher or lower risk


## Project Files

Capstone_analysis/
│
├── app.py
├── test_api.py
├── loan_model_bundle.joblib
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md

## File Descriptions
 - app.py: Contains the FastAPI application, request schema, model loading process, and prediction endpoints
 - test_api.py: Contains four unit tests for the API
 - loan_model_bundle.joblib: Contains the fitted preprocessor and optimized Random Forest Model
 - requirements.txt: Contains the list of the Python packages required to run the application
 - Dockerfile: Contains the definition of the Docker image utilized to package and run the API
 - .dockerignore: Prevents unnecessary files from being copied into the Docker image

 
 ## Prediction Process
 The API has the following sequence:
 1. JSON loan application
 2. Pydantic input validation
 3. One-row Pandas DataFrame
 4. Saved preprocessing transformation
 5. Optimized Random Forest Model
 6. Default probability and risk category


 ## Environment Compatibility 
 The saved model should be loaded with Python, along with the versions of packages that are compatible with the environment used during model training.


 ## Deployment Status
 The FastAPI application has been successfully tested within the following:
 - Locally with Uvicorn
 - Interactive FastAPI documentation
 - Four pytest unit tests
 - Inside a Docker container

 The project represents a local containerized deployment. It is not currently hosted at a publicly accessible web address.