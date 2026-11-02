import joblib
import pandas as pd
import os

def main():
    # 1. Load the trained model pipeline
    # (Change to final_model.joblib if you want to test the 2k model)
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "final_model_200k.joblib")
    
    if not os.path.exists(model_path):
        print("Model not found! Run training first.")
        return
        
    print("Loading model...")
    model = joblib.load(model_path)
    
    # 2. Create some "New" Fake Data (Must match the 15 features the 200k model expects)
    new_candidates = pd.DataFrame([
        {
            "age": 28,
            "education_level": "Masters",
            "university_tier": "Tier 1",
            "cgpa": 8.5,
            "internships": 2,
            "projects": 5,
            "programming_languages": 4,
            "certifications": 3,
            "experience_years": 3.5,
            "hackathons": 2,
            "research_papers": 1,
            "skills_score": 25.0,
            "soft_skills_score": 9.0,
            "resume_length_words": 500,
            "company_type": "MNC"
        },
        {
            "age": 22,
            "education_level": "Bachelors",
            "university_tier": "Tier 3",
            "cgpa": 5.5,
            "internships": 0,
            "projects": 1,
            "programming_languages": 1,
            "certifications": 0,
            "experience_years": 0.0,
            "hackathons": 0,
            "research_papers": 0,
            "skills_score": 5.0,
            "soft_skills_score": 4.0,
            "resume_length_words": 200,
            "company_type": "Startup"
        }
    ])
    
    print("\n--- New Candidates Data ---")
    print(new_candidates)
    
    # 3. Make Predictions
    # The pipeline automatically handles missing values, scaling, and categorical encoding!
    predictions = model.predict(new_candidates)
    
    print("\n--- Prediction Results ---")
    for i, pred in enumerate(predictions):
        status = "Hired / Selected" if pred == 1 else "Not Selected"
        print(f"Candidate {i+1}: {status}")

if __name__ == "__main__":
    main()
