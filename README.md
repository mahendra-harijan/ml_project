# Resume Selection Prediction System

An end-to-end Machine Learning pipeline and full-stack web application designed for screening candidate resumes and predicting hiring/selection probabilities using historical job-matching metrics and machine learning models.

---

## 📑 Table of Contents
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Step-by-Step Setup & Run Guide](#step-by-step-setup--run-guide)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Environment Configuration](#step-2-environment-configuration)
  - [Step 3: Setup & Run Backend (FastAPI)](#step-3-setup--run-backend-fastapi)
  - [Step 4: Setup & Run Frontend (React + Vite)](#step-4-setup--run-frontend-react--vite)
  - [Step 5 (Optional): ML Training & Pipeline Execution](#step-5-optional-ml-training--pipeline-execution)
- [API Endpoints](#api-endpoints)
- [Responsible AI & Ethical Notice](#responsible-ai--ethical-notice)

---

## 🏗 Architecture & Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Lucide Icons, Recharts, Axios
- **Backend**: FastAPI (Python), Uvicorn, PDFMiner.six, Pydantic
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
- **Database**: File-based Mock JSON / MongoDB ready

---

## 📁 Project Structure

```text
ML_Project/
├── backend/            # FastAPI REST API & PDF extraction service
│   ├── app/            # Application logic, routes, and services
│   └── requirements.txt# Python dependencies for the backend
├── frontend/           # React + Vite user interface
│   ├── src/            # Components, pages, and UI styles
│   └── package.json    # Node dependencies and build scripts
├── ml/                 # Machine Learning pipeline
│   ├── data/           # Dataset folders (demo / raw / processed)
│   ├── models/         # Trained model binaries and version configs
│   ├── src/            # Training, preprocessing & evaluation scripts
│   └── requirements.txt# Python dependencies for ML scripts
├── docs/               # Detailed architectural and workflow documentation
├── .env.example        # Template for environment variables
└── README.md           # Project guide
```

---

## ⚙️ Prerequisites

Before running this project, ensure you have installed:
- **Python 3.10+** ([Download Python](https://www.python.org/downloads/))
- **Node.js 18+ & npm** ([Download Node.js](https://nodejs.org/))
- **Git** ([Download Git](https://git-scm.com/))

---

## 🚀 Step-by-Step Setup & Run Guide

### Step 1: Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd ML_Project
```

### Step 2: Environment Configuration
Create a `.env` file from the provided example template:
- **Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
- **Linux / macOS:**
  ```bash
  cp .env.example .env
  ```

---

### Step 3: Setup & Run Backend (FastAPI)

Open a terminal at the project root:

1. **Create and activate a virtual environment**:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
     *(If script execution is disabled in PowerShell, first run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **Install backend dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```

3. **Start the FastAPI server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```
   - API will be accessible at: `http://localhost:8000`
   - Interactive Swagger API docs: `http://localhost:8000/docs`

---

### Step 4: Setup & Run Frontend (React + Vite)

Open a **new terminal window** in the project root:

1. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   ```

2. **Install NPM dependencies**:
   ```bash
   npm install
   ```

3. **Start the Vite development server**:
   ```bash
   npm run dev
   ```
   - Web application will run at: `http://localhost:5173`

---

### Step 5 (Optional): ML Training & Pipeline Execution

To retrain the machine learning models:

1. Activate your virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. Install ML requirements:
   ```bash
   pip install -r ml/requirements.txt
   ```

3. Train the model:
   ```bash
   python ml/src/train.py
   ```
   Or for the 200k record dataset:
   ```bash
   python ml/src/train_200k.py
   ```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check & system status |
| `POST` | `/api/screen` | Upload resume PDF & target job description to get match prediction |
| `GET` | `/api/dashboard` | Retrieve summary statistics and historical screening results |

---

## ⚖️ Responsible AI & Ethical Notice

This system demonstrates technical architecture and machine learning workflow principles. It uses synthetic training data and heuristic feature extraction; **do not use this system as the sole decision-maker for real-world recruitment or hiring.**
