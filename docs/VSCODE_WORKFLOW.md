# VS Code Workflow

## 1. Open Project
Open the `resume-selection-predictor` folder in VS Code.

## 2. Create Python Environment
Run in terminal:
```powershell
python -m venv venv
```

## 3. Activate Environment
```powershell
.\venv\Scripts\activate
```

## 4. Install ML and Backend Requirements
```powershell
pip install -r backend/requirements.txt
```

## 5. Train Model
```powershell
python ml/src/train.py
```
This will output `final_model.joblib` and `model_version.json` in `ml/models`.

## 6. Start Backend
In a new terminal (with venv activated):
```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```

## 7. Start Frontend
In a new terminal:
```powershell
cd frontend
npm run dev
```

## 8. Open Browser
Navigate to `http://localhost:5173` (or the port Vite provides) to test the application.

## 9. Run Tests
```powershell
pytest backend/app/test_main.py
```
