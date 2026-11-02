import os
import joblib
import pandas as pd

class ResumePredictor:
    def __init__(self, models_dir=None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
            
        self.model_path = os.path.join(models_dir, "final_model.joblib")
        self.preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")
        
        if not os.path.exists(self.model_path) or not os.path.exists(self.preprocessor_path):
            raise FileNotFoundError("Model or preprocessor not found. Please train the model first.")
            
        self.model = joblib.load(self.model_path)
        self.preprocessor = joblib.load(self.preprocessor_path)
        
    def predict(self, features_dict):
        df = pd.DataFrame([features_dict])
        
        # Ensure all expected columns are present, using default values if missing
        expected_cols = [
            'education', 'cgpa', 'experience_years', 'internship_count', 
            'project_count', 'certification_count', 'skills_match_score', 
            'relevant_skill_count', 'job_role'
        ]
        
        for col in expected_cols:
            if col not in df.columns:
                if col in ['education', 'job_role']:
                    df[col] = 'Unknown'
                else:
                    df[col] = 0
                    
        X_processed = self.preprocessor.transform(df)
        
        prediction = self.model.predict(X_processed)[0]
        
        probability = None
        if hasattr(self.model, 'predict_proba'):
            probability = self.model.predict_proba(X_processed)[0][1]
            
        return {
            'prediction': int(prediction),
            'probability': float(probability) if probability is not None else None
        }

if __name__ == "__main__":
    # Test inference
    predictor = ResumePredictor()
    test_features = {
        'education': 'Masters',
        'cgpa': 3.8,
        'experience_years': 5,
        'internship_count': 2,
        'project_count': 5,
        'certification_count': 3,
        'skills_match_score': 85.0,
        'relevant_skill_count': 8,
        'job_role': 'Software Engineer'
    }
    result = predictor.predict(test_features)
    print(f"Prediction result: {result}")
