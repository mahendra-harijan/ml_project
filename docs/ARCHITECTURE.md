# System Architecture

## Overview
The application is a standard modern 3-tier web application split into Frontend, Backend API, and a Machine Learning Engine, utilizing a Document Database (MongoDB) for persistence.

## Components
1. **Frontend (React + Vite)**: 
   - Uses Tailwind CSS for rapid styling.
   - Communicates asynchronously via Axios to the FastAPI backend.
   - Hosted statically or via Vite dev server locally.

2. **Backend (FastAPI)**:
   - High-performance API using `uvicorn`.
   - Handles PDF parsing via `pdfminer.six`.
   - Implements Job Description matching logic using rule-based/regex extraction.
   - Routes prediction requests to the Machine Learning Engine.

3. **ML Engine (Scikit-Learn)**:
   - Contains a preprocessing pipeline (handling missing values, scaling, one-hot encoding).
   - Serves the `final_model.joblib` artifact.
   - In production, it evaluates candidate features in milliseconds.

4. **Database (MongoDB)**:
   - Collections: `predictions`.
   - Stores candidate features, predictions, and parsed metrics for Dashboard visualization.
   - Fallback locally to a JSON file if MongoDB is unreachable.
