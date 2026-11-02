import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from data_preprocessing import build_preprocessor
from evaluate import evaluate_model
import joblib
from datetime import datetime

def train_models():
    print("Training started...")
    
    # Load dataset
    data_path = os.path.join("..", "data", "demo", "demo_synthetic_resume_selection.csv")
    df = pd.read_csv(data_path)
    
    print(f"Dataset:\nRecords: {len(df)}")
    
    X = df.drop(columns=['selected'])
    y = df['selected']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    preprocessor, _, _ = build_preprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    models = {
        "Logistic Regression": LogisticRegression(random_state=42, max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "SVM": SVC(probability=True, random_state=42)
    }
    
    print("\nModels:")
    results = []
    
    best_f1 = 0
    best_model_name = None
    best_model = None
    
    for i, (name, model) in enumerate(models.items(), 1):
        print(f"[{i}/4] {name}")
        model.fit(X_train_processed, y_train)
        
        metrics = evaluate_model(model, X_test_processed, y_test)
        metrics['Model'] = name
        results.append(metrics)
        
        if metrics['F1'] > best_f1:
            best_f1 = metrics['F1']
            best_model_name = name
            best_model = model
            
    print("\nEvaluation complete.")
    
    # Save comparison report
    results_df = pd.DataFrame(results)
    
    reports_dir = os.path.join("..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    results_df.to_csv(os.path.join(reports_dir, "model_comparison.csv"), index=False)
    
    print(f"\nBest model: {best_model_name}")
    print(f"F1 Score: {best_f1:.4f}")
    
    # Save best model and preprocessor
    models_dir = os.path.join("..", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(best_model, os.path.join(models_dir, "final_model.joblib"))
    joblib.dump(preprocessor, os.path.join(models_dir, "preprocessor.joblib"))
    
    print(f"\nModel saved:\n{os.path.join('ml', 'models', 'final_model.joblib')}")
    
    # Save metadata
    metadata = {
        "model_name": best_model_name,
        "version": "1.0.0",
        "trained_at": datetime.now().isoformat(),
        "dataset": "demo_synthetic_resume_selection.csv",
        "training_records": len(X_train),
        "metrics": next(m for m in results if m['Model'] == best_model_name)
    }
    with open(os.path.join(models_dir, "model_version.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
if __name__ == "__main__":
    # Change working dir to script directory to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    train_models()
