import os

directories = [
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/layouts",
    "frontend/src/services",
    "frontend/src/hooks",
    "frontend/src/utils",
    "frontend/src/assets",
    "frontend/public",
    "backend/app/routes",
    "backend/app/services",
    "backend/app/schemas",
    "backend/app/utils",
    "backend/app/config",
    "ml/data/raw",
    "ml/data/processed",
    "ml/data/demo",
    "ml/notebooks",
    "ml/src",
    "ml/models",
    "ml/reports",
    "docs",
    "scripts/setup",
    "scripts/train",
    "scripts/run"
]

files = {
    "frontend/package.json": "{\n  \"name\": \"frontend\",\n  \"version\": \"1.0.0\"\n}",
    "frontend/README.md": "# Frontend\n",
    "backend/app/main.py": "",
    "backend/requirements.txt": "fastapi\nuvicorn\npydantic\npymongo\npython-multipart\npdfminer.six\njoblib\nscikit-learn\npandas\nnumpy\n",
    "backend/README.md": "# Backend\n",
    "ml/data/README.md": "# Dataset documentation\n",
    "ml/src/data_preprocessing.py": "",
    "ml/src/feature_engineering.py": "",
    "ml/src/train.py": "",
    "ml/src/evaluate.py": "",
    "ml/src/predict.py": "",
    "ml/src/utils.py": "",
    "ml/requirements.txt": "pandas\nnumpy\nscikit-learn\njoblib\nmatplotlib\n",
    "ml/README.md": "# ML Pipeline\n",
    "docs/ARCHITECTURE.md": "# Architecture\n",
    "docs/ML_PIPELINE.md": "# ML Pipeline\n",
    "docs/API_DOCUMENTATION.md": "# API Documentation\n",
    "docs/DATABASE.md": "# Database\n",
    "docs/TRAINING_GUIDE.md": "# Training Guide\n",
    "docs/DEPLOYMENT.md": "# Deployment\n",
    "docs/TROUBLESHOOTING.md": "# Troubleshooting\n",
    ".env.example": "MONGO_URI=mongodb://localhost:27017\n",
    ".gitignore": "node_modules/\n__pycache__/\n*.pyc\n.env\nvenv/\nml/models/*.joblib\nml/data/raw/*.csv\nml/data/processed/*.csv\n",
    "README.md": "# Resume Selection Prediction System\n",
    "docker-compose.yml": "version: '3.8'\nservices:\n  mongodb:\n    image: mongo:latest\n    ports:\n      - \"27017:27017\"\n"
}

for d in directories:
    os.makedirs(d, exist_ok=True)

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Project structure created successfully.")
