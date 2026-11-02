from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.pdf_service import extract_text_from_pdf, extract_information
from app.services.match_service import process_job_description, calculate_skill_match
import os
import shutil
import sys
import json
from datetime import datetime
from pymongo import MongoClient

# Ensure ml modules can be imported
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ml", "src"))
try:
    from predict import ResumePredictor
    predictor = ResumePredictor(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ml", "models"))
except Exception as e:
    print(f"Warning: Model not loaded properly. {e}")
    predictor = None

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = client.resume_db
    predictions_collection = db.predictions
except Exception as e:
    print(f"Warning: Could not connect to MongoDB: {e}")
    db = None

router = APIRouter()

@router.post("/predict/resume")
async def predict_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    global predictor
    if not resume.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    temp_path = f"temp_{resume.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
        
    try:
        resume_text = extract_text_from_pdf(temp_path)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Empty or unreadable PDF")
            
        candidate_info = extract_information(resume_text)
        
        jd_data = process_job_description(job_description)
        match_data = calculate_skill_match(resume_text, jd_data['required_skills'])
        
        candidate_info['skills'] = match_data['matched_skills']
        
        features = {
            'education': candidate_info['education'],
            'cgpa': candidate_info['cgpa'],
            'experience_years': candidate_info['experience_years'],
            'internship_count': candidate_info['internships'],
            'project_count': candidate_info['projects'],
            'certification_count': candidate_info['certifications'],
            'skills_match_score': match_data['match_score'],
            'relevant_skill_count': len(match_data['matched_skills']),
            'job_role': jd_data['role']
        }
        
        if predictor is None:
            try:
                from predict import ResumePredictor
                predictor = ResumePredictor(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ml", "models"))
            except Exception:
                raise HTTPException(status_code=500, detail="ML model is not loaded.")
            
        prediction_result = predictor.predict(features)
        
        model_version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ml", "models", "model_version.json")
        model_name = "Unknown"
        model_version = "1.0"
        if os.path.exists(model_version_path):
            with open(model_version_path, "r") as f:
                v = json.load(f)
                model_name = v.get("model_name", model_name)
                model_version = v.get("version", model_version)
        
        record = {
            "prediction": "Selected" if prediction_result['prediction'] == 1 else "Not Selected",
            "probability": prediction_result['probability'],
            "model": model_name,
            "model_version": model_version,
            "skill_match_score": match_data['match_score'],
            "matched_skills": match_data['matched_skills'],
            "missing_skills": match_data['missing_skills'],
            "candidate": candidate_info,
            "created_at": datetime.now().isoformat()
        }
        
        # Save to MongoDB
        if db is not None:
            try:
                predictions_collection.insert_one(record.copy()) # copy because pymongo adds _id
            except Exception as e:
                print(f"Error saving to MongoDB: {e}")
        else:
            # Fallback mock DB
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "predictions.json")
            local_db = []
            if os.path.exists(db_path):
                with open(db_path, "r") as f:
                    local_db = json.load(f)
            local_db.append(record)
            with open(db_path, "w") as f:
                json.dump(local_db, f)
        
        record["disclaimer"] = "This is a model-generated prediction and not a guaranteed hiring decision."
        if "_id" in record:
            record["_id"] = str(record["_id"])
            
        return record
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/predictions")
async def get_predictions():
    if db is not None:
        try:
            cursor = predictions_collection.find().sort("created_at", -1).limit(50)
            preds = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                preds.append(doc)
            return preds
        except Exception as e:
            print(e)
            
    # Fallback mock DB
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "predictions.json")
    if os.path.exists(db_path):
        with open(db_path, "r") as f:
            return json.load(f)
    return []

@router.get("/model/info")
async def get_model_info():
    model_version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ml", "models", "model_version.json")
    if os.path.exists(model_version_path):
        with open(model_version_path, "r") as f:
            return json.load(f)
    return {"message": "Model information not available"}

@router.get("/model/metrics")
async def get_model_metrics():
    metrics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "ml", "reports", "model_comparison.csv")
    if os.path.exists(metrics_path):
        import pandas as pd
        df = pd.read_csv(metrics_path)
        return df.to_dict(orient="records")
    return []
