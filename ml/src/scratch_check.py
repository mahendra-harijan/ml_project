import joblib
import pandas as pd
import os

model_path = os.path.join(os.path.dirname(__file__), "..", "models", "final_model_200k.joblib")
model = joblib.load(model_path)

# Create extreme negative case
test_data = pd.DataFrame([{
    "age": 100,
    "education_level": "Bachelors",
    "university_tier": "Tier 5",
    "cgpa": -100.0,
    "internships": -100,
    "projects": -100,
    "programming_languages": -100,
    "certifications": -100,
    "experience_years": -100.0,
    "hackathons": -100,
    "research_papers": -100,
    "skills_score": -1000.0,
    "soft_skills_score": -1000.0,
    "resume_length_words": 0,
    "company_type": "Startup"
}])

pred = model.predict(test_data)
prob = model.predict_proba(test_data)
print(f"Prediction: {pred[0]}, Proba: {prob[0]}")
