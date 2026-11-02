import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import time

def main():
    print("Starting training process on 200k enhanced dataset...")
    start_time = time.time()
    
    # 1. Load Data
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "demo", "resume_dataset_200k_enhanced.csv")
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return
        
    print("Loading data...")
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} records.")
    
    # 2. Define Features and Target
    target_col = 'hired'
    
    # Exclude candidate_id from training
    feature_cols = [c for c in df.columns if c not in [target_col, 'candidate_id']]
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 3. Identify categorical and numeric columns
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
    
    print(f"Numeric features: {len(numeric_cols)}")
    print(f"Categorical features: {len(categorical_cols)}")
    
    # 4. Preprocessing Pipeline
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )
    
    # 5. Train-Test Split (using a smaller test set due to large data size)
    print("Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Since 200k is quite large, SVM might take a very long time. 
    # We will limit SVM or remove it if we want fast execution, but let's keep a fast variant.
    # LinearSVC is much faster than SVC for large datasets.
    from sklearn.svm import LinearSVC
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "Decision Tree": DecisionTreeClassifier(random_state=42, class_weight='balanced'),
        "Random Forest": RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1, class_weight='balanced'),
        "Linear SVM": LinearSVC(max_iter=1000, random_state=42, class_weight='balanced')
    }
    
    results = []
    best_f1 = 0
    best_model_name = ""
    best_pipeline = None
    
    # 6. Train and Evaluate Models
    for name, model in models.items():
        print(f"\nTraining {name}...")
        clf = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])
        
        clf.fit(X_train, y_train)
        
        print(f"Evaluating {name}...")
        y_pred = clf.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # ROC-AUC needs probabilities. LinearSVC doesn't have predict_proba by default.
        if hasattr(clf.named_steps['classifier'], "predict_proba"):
            y_prob = clf.predict_proba(X_test)[:, 1]
            roc = roc_auc_score(y_test, y_prob)
        elif hasattr(clf.named_steps['classifier'], "decision_function"):
            y_prob = clf.decision_function(X_test)
            roc = roc_auc_score(y_test, y_prob)
        else:
            roc = 0.0
            
        print(f"{name} -> Acc: {acc:.4f}, F1: {f1:.4f}, ROC: {roc:.4f}")
        
        results.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1": round(f1, 4),
            "ROC-AUC": round(roc, 4)
        })
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = clf

    # 7. Save Reports
    reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    report_df = pd.DataFrame(results)
    report_df = report_df[['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC', 'Model']]
    
    report_path = os.path.join(reports_dir, "model_comparison_200k.csv")
    report_df.to_csv(report_path, index=False)
    print(f"\nSaved report to {report_path}")
    
    # 8. Save Models
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"\nBest model found: {best_model_name} (F1: {best_f1:.4f})")
    
    # Save the full pipeline as final_model_200k.joblib
    model_path = os.path.join(models_dir, "final_model_200k.joblib")
    joblib.dump(best_pipeline, model_path)
    print(f"Saved best pipeline to {model_path}")
    
    # Save version info
    version_info = {
        "model_name": best_model_name,
        "dataset": "resume_dataset_200k_enhanced.csv",
        "version": "1.0_200k",
        "training_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "metrics": {
            "f1_score": best_f1
        }
    }
    
    version_path = os.path.join(models_dir, "model_version_200k.json")
    with open(version_path, "w") as f:
        json.dump(version_info, f, indent=4)
        
    print(f"Training completed in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
