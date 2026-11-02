# API Documentation

## Base URL
`http://localhost:8000/api`

## Endpoints

### 1. `GET /health`
Returns the status of the API server.
**Response**: `{"status": "healthy"}`

### 2. `POST /predict/resume`
Uploads a resume and job description, extracts info, and returns a prediction.
- **Parameters**: 
  - `resume`: PDF file (multipart/form-data)
  - `job_description`: string (form data)
- **Response**: JSON object containing candidate info, skill match, prediction, and probability.

### 3. `GET /predictions`
Fetches a list of recent predictions.
- **Response**: List of JSON objects with historical candidate records.

### 4. `GET /model/info`
Fetches metadata about the currently loaded ML model.
- **Response**: JSON object (e.g., `{"model_name": "Logistic Regression", "version": "1.0.0", ...}`)

### 5. `GET /model/metrics`
Fetches the evaluation metrics (Accuracy, F1, etc.) for all trained models.
- **Response**: List of JSON objects representing model comparisons.
