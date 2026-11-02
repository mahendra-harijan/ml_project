# Resume Selection Prediction System

## Overview
A complete, end-to-end Machine Learning pipeline and web application for screening resumes and predicting candidate selection probabilities based on historical patterns (using a synthetic demo dataset).

## Features
- **PDF Resume Upload**: Extract text and candidate information from uploaded PDF resumes.
- **Job Description Matching**: Calculate a skill match score based on extracted requirements.
- **Machine Learning Inference**: Evaluate the candidate using an automated feature pipeline and a trained Scikit-Learn model.
- **Interactive Dashboard**: View historical predictions and model performance metrics.
- **Responsible AI Considerations**: Transparent probability scoring and warnings about automated decisions.

## Architecture
- **Frontend**: React, Vite, Tailwind CSS, Recharts
- **Backend**: FastAPI (Python), uvicorn, pdfminer.six
- **Machine Learning**: Scikit-Learn, pandas, joblib
- **Database**: File-based JSON Mock (MongoDB placeholder for demo purposes without external DB dependency).

## Project Structure
- `/frontend`: React application
- `/backend`: FastAPI backend and services
- `/ml`: Machine Learning pipeline, notebooks, and models
- `/docs`: Extensive documentation

## Installation
Please refer to `docs/TRAINING_GUIDE.md` and `docs/VSCODE_WORKFLOW.md` for complete installation instructions.

## Ethical Considerations
This system uses a **synthetic demo dataset** due to the lack of real-world datasets with objective "Selected" labels. It serves as a technical architecture demonstration. Do not use this model for actual hiring decisions.

## Limitations
- Extraction uses regex and basic heuristics rather than advanced NER.
- Database is mocked to local JSON to avoid complex local MongoDB setup issues, though the architecture supports swapping to PyMongo seamlessly.
- Model decisions are based on synthetic data.


Run Command
1).\venv\Scripts\Activate.ps1
2)cd backend
uvicorn app.main:app --reload --port 8000

