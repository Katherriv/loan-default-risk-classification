FROM python:3.14.5

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir \
    --upgrade pip \
    && python -m pip install \
    --no-cache-dir \
    -r requirements.txt

COPY app.py .
COPY loan_model_bundle.joblib .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]