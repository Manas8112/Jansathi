# Setup script for JanSaathi Teammates

Write-Host "Setting up JanSaathi project..."

# 1. Install Frontend dependencies
Write-Host "Installing Frontend Dependencies..."
cd frontend
npm install
cd ..

# 2. Install Backend dependencies
Write-Host "Installing Backend Dependencies..."
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install --prefer-binary -r requirements.txt  # --prefer-binary avoids Rust/MSVC build tools

Write-Host ""
Write-Host "========================================="
Write-Host "Setup Complete!"
Write-Host "To run the app:"
Write-Host "1. In one terminal, run: cd frontend ; npm run dev"
Write-Host "2. In another terminal, run: cd backend ; .\.venv\Scripts\activate ; uvicorn main:app --reload"
Write-Host ""
Write-Host "NOTE ON API KEYS:"
Write-Host "Since the actual Groq API key is kept secret, you MUST provide your own."
Write-Host "Navigate to the backend/ folder, rename '.env.example' to '.env', and paste your free Groq API key inside."
Write-Host ""
Write-Host "NOTE ON THE LOCAL ML MODEL:"
Write-Host "The trained model (430MB) is tracked via Git LFS."
Write-Host "If you did not use Git LFS when cloning, the model file is a tiny pointer and the backend will fall back to the cloud."
Write-Host "To train the model yourself locally (takes ~4 mins), run:"
Write-Host "cd backend ; .\.venv\Scripts\activate ; python training/download_datasets.py ; python training/intent_classifier.py"
Write-Host "========================================="
