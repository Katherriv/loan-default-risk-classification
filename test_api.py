from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

#Testing the API status endpoint returns a successful response
def test_api_status_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.json()

#Testing that the prediction endpoint accepts a correctly formatted request
def test_predict_default_valid_request():
    response = client.post(
        "/predict/default-risk",
        json = {
            'loan_amount': 116500,
            'term': 360,
            'income': 1740,
            'Credit_Score': 758,
            'LTV': 98.72881356,
            'dtir1': 45,
            'credit_type': 'EXP',
            'loan_type': 'type1',
            'loan_purpose': 'p1',
            'loan_limit': 'cf',
            'approv_in_adv': 'nopre',
            'Credit_Worthiness': 'l1',
            'business_or_commercial': 'nob/c',
            'Neg_ammortization': 'not_neg',
            'interest_only': 'not_int',
            'lump_sum_payment': 'not_lpsm',
            'age': '25-34',
            'submission_of_application': 'to_inst',
            'occupancy_type': 'pr',
            'Region': 'south'})

    assert response.status_code == 200

    data = response.json()

    assert 'default_probability' in data
    assert 'predict_status' in data
    assert 'risk_category' in data

#Testing an incorrectly formatted request returns a 422 error (loan amount misspelled)
def test_predict_invalid_request():
    response = client.post(
        "/predict/default-risk",
        json = {
            'loan_amnt': 116500,
            'term': 360,
            "income": 1740,
            "Credit_Score": 758,
            "LTV": 98.72881356,
            "dtir1": 45,
            "credit_type": "EXP",
            "loan_type": "type1",
            "loan_purpose": "p1",
            "loan_limit": "cf",
            "approv_in_adv": "nopre",
            "Credit_Worthiness": "l1",
            "business_or_commercial": "nob/c",
            "Neg_ammortization": "not_neg",
            "interest_only": "not_int",
            "lump_sum_payment": "not_lpsm",
            "age": "25-34",
            "submission_of_application": "to_inst",
            "occupancy_type": "pr",
            "Region": "south"})

    assert response.status_code == 422

#Testing a missing entry in request, returnning a 422 error (missing occupancy_type)
def test_predict_missing_request():
    response = client.post(
        "/predict/default-risk",
        json = {
           'loan_amount': 116500,
            'term': 360,
            "income": 1740,
            "Credit_Score": 758,
            "LTV": 98.72881356,
            "dtir1": 45,
            "credit_type": "EXP",
            "loan_type": "type1",
            "loan_purpose": "p1",
            "loan_limit": "cf",
            "approv_in_adv": "nopre",
            "Credit_Worthiness": "l1",
            "business_or_commercial": "nob/c",
            "Neg_ammortization": "not_neg",
            "interest_only": "not_int",
            "lump_sum_payment": "not_lpsm",
            "age": "25-34",
            "submission_of_application": "to_inst",
            "Region": "south"})

    assert response.status_code == 422