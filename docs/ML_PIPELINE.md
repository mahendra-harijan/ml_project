# ML Pipeline

## Dataset
The project uses a generated synthetic dataset to demonstrate the complete workflow. It includes columns for candidate education, CGPA, experience, and skill matching, mapped to a simulated "Selected" (1/0) label. 

## Preprocessing
- **Numeric Features**: Imputed using median, scaled using StandardScaler.
- **Categorical Features**: Imputed using most frequent, encoded using OneHotEncoder.

## Models
1. **Logistic Regression**
2. **Decision Tree**
3. **Random Forest**
4. **SVM (Support Vector Machine)**

## Training Process
The dataset is split 80/20. All 4 models are trained and evaluated. The model with the highest F1-Score is saved as `final_model.joblib`.

## Evaluation
Metrics captured include Accuracy, Precision, Recall, F1, and ROC-AUC. Results are saved to `model_comparison.csv`.
