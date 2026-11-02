# Troubleshooting

## Model Fails to Load
- **Error**: `FileNotFoundError: Model or preprocessor not found.`
- **Solution**: Ensure you have run `python ml/src/train.py` from the root directory so the pipeline creates `.joblib` files in `ml/models`.

## Database Connection Error
- **Error**: `Warning: Could not connect to MongoDB`
- **Solution**: The application gracefully falls back to a local JSON file (`backend/predictions.json`). To use MongoDB, ensure the server is running (e.g. `docker-compose up -d`) and `MONGO_URI` is correctly set.

## Frontend Cannot Connect to API
- **Error**: `Network Error` on the Dashboard or Screening page.
- **Solution**: Ensure the FastAPI server is running on `http://localhost:8000`. If you changed the port, update the Axios calls in `frontend/src/pages/`.

## Empty PDF Extraction
- **Error**: `Empty or unreadable PDF`
- **Solution**: The uploaded PDF might be an image-based scan. `pdfminer.six` only extracts text from standard text-based PDFs. You may need to integrate OCR (like Tesseract) for scanned resumes.
