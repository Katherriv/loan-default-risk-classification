from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

#Loading deployment bundle
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "loan_model_bundle.joblib"

try:
    deploy_bundle = joblib.load(MODEL_PATH)
except FileNotFoundError as exc:
    raise RuntimeError(
        f"Model bundle not found at: {MODEL_PATH}") from exc
except Exception as exc:
    raise RuntimeError(
        'The model bundle could not be loaded. '
        'Confirming Python and package versions match model_training environment.') from exc

require_keys = {
    'preprocessor', 'model', 'raw_feature_names'}

miss_keys = require_keys - set(deploy_bundle)

if miss_keys:
    raise RuntimeError(
        f'Deployment bundle missing required items: '
        f'{sorted(miss_keys)}')

preprocessor = deploy_bundle['preprocessor']
model = deploy_bundle['model']
raw_feature_names = deploy_bundle['raw_feature_names']

#Locating probability column relating to Status = 1
model_classes = list(model.classes_)

if 1 not in model_classes:
    raise RuntimeError(
        'Loaded model does not contain Status = 1 as a prediction class.')

default_class_ind = model_classes.index(1)

#Input and output schemas
class LoanApplication(BaseModel):
    #Raw loan appl inputs expected by saved processor and model
    model_config = ConfigDict(
        extra = 'forbid',
        json_schema_extra = {
            'example': {
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
                'Region': 'south'}})

    #Numeric inputs
    loan_amount: float
    term: float
    income: float
    Credit_Score: float
    LTV: float
    dtir1: float

    #Categorical inputs
    credit_type: str
    loan_type: str
    loan_purpose: str
    loan_limit: str
    approv_in_adv: str
    Credit_Worthiness: str
    business_or_commercial: str
    Neg_ammortization: str
    interest_only: str
    lump_sum_payment: str
    age: str
    submission_of_application: str
    occupancy_type: str
    Region: str

class PredictionResponse(BaseModel):
    default_probability: float
    predict_status: int
    risk_category: str


#FastAPI application

app = FastAPI(
    title = 'Loan Default Risk Prediction API',
    description = ('Utilizes an optimized Random Forest classifier to predict loan default risk.'),
    version = '1.0.0')

@app.get("/")
def api_status() -> dict[str, str]:
    """Confirming that API is functional."""

    return {
        'message': (
            'Loan default risk prediction API is functional.')}

@app.post(
    "/predict/default-risk",
    response_model = PredictionResponse)
def predict_default(
    application: LoanApplication) -> PredictionResponse:
    """
    Predict the probability and risk of loan default.
    """

    try:
        #Converting Pydantic input into dict
        input_values = application.model_dump()

        #Converting one application into 1 row df
        input_df = pd.DataFrame([input_values])

        #Putting columns in expected order by fitted processor
        input_df = input_df[raw_feature_names]

        #Applying saved preprocessing
        process_input = preprocessor.transform(input_df)

        #Generating predicted class
        predict_status = int(
            model.predict(process_input)[0])

        #Generating probability of Status = 1
        default_probability = float(
            model.predict_proba(process_input)[0, default_class_ind])

    except Exception as exc:
        raise HTTPException(
            status_code = 500,
            detail = "Loan default prediction failed."
        ) from exc
    
    risk_category = (
        'Higher default risk'
        if predict_status == 1
        else 'Lower default risk')

    return PredictionResponse(
        default_probability = round(default_probability, 4),
        predict_status = predict_status, risk_category = risk_category)
