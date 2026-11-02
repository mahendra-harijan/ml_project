# Training Guide

## STEP 1: Install Python
Ensure Python 3.9+ is installed.

## STEP 2: Create virtual environment
```powershell
python -m venv venv
```

## STEP 3: Install ML dependencies
```powershell
.\venv\Scripts\activate
pip install -r backend/requirements.txt
```

## STEP 4: Download/prepare dataset
By default, the synthetic dataset generator handles this.

## STEP 5: Put dataset in correct directory
The generator places it in `ml/data/demo/demo_synthetic_resume_selection.csv`.

## STEP 6: Validate dataset
Verify the dataset contains the `selected` target column.

## STEP 7: Run preprocessing
Preprocessing is built into the training pipeline.

## STEP 8: Train four models
```powershell
python ml/src/train.py
```

## STEP 9: Compare metrics
Review `ml/reports/model_comparison.csv`.

## STEP 10: Select final model
The script automatically selects the best model by F1-Score.

## STEP 11: Save model
The model is saved to `ml/models/final_model.joblib`.

## STEP 12: Start FastAPI
```powershell
cd backend
uvicorn app.main:app --reload
```

## STEP 13: Connect frontend
```powershell
cd frontend
npm run dev
```

## STEP 14: Test prediction
Navigate to localhost:5173, upload a PDF and analyze it.
