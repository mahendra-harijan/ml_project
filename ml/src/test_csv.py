import joblib
import pandas as pd
import os

def main():
    print("--- Step 1: Loading Model ---")
    model_path = os.path.join(os.path.dirname(__file__), "..", "models", "final_model_200k.joblib")
    model = joblib.load(model_path)
    print(f"Successfully loaded {model_path}")
    
    print("\n--- Step 2: Loading New Data (CSV) ---")
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "demo", "test_sample_data.csv")
    new_data = pd.read_csv(csv_path)
    
    # Show the first few columns so the user can see what was loaded
    print(new_data[['age', 'education_level', 'cgpa', 'experience_years']])
    
    print("\n--- Step 3: Making Predictions ---")
    # Feed the entire CSV into the model at once
    predictions = model.predict(new_data)
    
    # Attach predictions back to the dataframe for easy viewing
    new_data['PREDICTED_STATUS'] = ["Selected" if p == 1 else "Not Selected" for p in predictions]
    
    print("\n--- Final Results ---")
    # Print out a clean summary
    results = new_data[['education_level', 'cgpa', 'experience_years', 'PREDICTED_STATUS']]
    print(results.to_string(index=False))

if __name__ == "__main__":
    main()
