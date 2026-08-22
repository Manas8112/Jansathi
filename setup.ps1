# Setup script for JanSaathi Teammates

Write-Host "Setting up JanSaathi project..."

# 1. Fetch AI Models (Git LFS)
Write-Host "Fetching trained AI models (this may take a minute)..."
try {
    git lfs install
    git lfs pull
    Write-Host "Models downloaded successfully!"
} catch {
    Write-Host "WARNING: Git LFS not found or failed to pull. The local intent router may fall back to the cloud."
}

# 2. Install Frontend dependencies
Write-Host "Installing Frontend Dependencies..."
cd frontend
npm install
cd ..

# 3. Install Backend dependencies
Write-Host "Installing Backend Dependencies..."
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

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
Write-Host "The trained model (430MB) is fetched automatically via Git LFS."
Write-Host "If it failed, ensure you have Git LFS installed and run 'git lfs pull'."
Write-Host "To train the model yourself locally (takes ~4 mins), run:"
Write-Host "cd backend ; .\.venv\Scripts\activate ; python training/download_datasets.py ; python training/intent_classifier.py"
Write-Host "========================================="
