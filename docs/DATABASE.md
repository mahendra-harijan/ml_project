# Database Schema

## Overview
The application connects to a MongoDB instance defined by `MONGO_URI` (defaults to `mongodb://localhost:27017`). If unavailable, it falls back to a local `predictions.json` file for resilience.

## Collections

### `predictions`
Stores evaluation results and candidate metadata.
```json
{
  "_id": "ObjectId",
  "prediction": "Selected",
  "probability": 0.88,
  "model": "Logistic Regression",
  "model_version": "1.0.0",
  "skill_match_score": 85.0,
  "matched_skills": ["python", "react"],
  "missing_skills": ["aws"],
  "candidate": {
    "name": "Candidate Name",
    "email": "test@example.com",
    "education": "Masters",
    "cgpa": 3.5,
    "experience_years": 4,
    "internships": 1,
    "projects": 3,
    "certifications": 2
  },
  "created_at": "2023-10-27T10:00:00.000Z",
  "disclaimer": "..."
}
```
