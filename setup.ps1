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
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================="
Write-Host "Setup Complete!"
Write-Host "To run the app:"
Write-Host "1. In one terminal, run: cd frontend ; npm run dev"
Write-Host "2. In another terminal, run: cd backend ; .\.venv\Scripts\activate ; uvicorn main:app --reload"
Write-Host "========================================="
