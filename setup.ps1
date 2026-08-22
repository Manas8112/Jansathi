[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Setup script for JanSaathi Teammates
$baseDir = $PSScriptRoot

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
cd "$baseDir\frontend"
npm install

# 3. Install Backend dependencies
Write-Host "Installing Backend Dependencies..."
cd "$baseDir\backend"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================="
Write-Host "Setup Complete!"

# Ask for Groq API Key
Write-Host ""
$groqKey = Read-Host "Please enter your Groq API Key (or press Enter to skip)"
if (-not [string]::IsNullOrWhiteSpace($groqKey)) {
    # Ensure it's written in UTF-8
    $envPath = "$baseDir\backend\.env"
    "GROQ_API_KEY=$groqKey" | Out-File -FilePath $envPath -Encoding UTF8
    Write-Host "Saved Groq API Key to backend/.env"
} else {
    Write-Host "Skipped. You will need to manually add GROQ_API_KEY to backend/.env if you didn't already."
}

Write-Host ""
Write-Host "The trained model (430MB) is fetched automatically via Git LFS."
Write-Host "If it failed, ensure you have Git LFS installed and run 'git lfs pull'."
Write-Host "To train the model yourself locally (takes ~4 mins), run:"
Write-Host "cd backend ; .\.venv\Scripts\activate ; python training/download_datasets.py ; python training/intent_classifier.py"
Write-Host "========================================="

Write-Host "Starting Frontend and Backend in new terminals..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$baseDir\frontend`"; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$baseDir\backend`"; .\`.venv\Scripts\activate; uvicorn main:app --reload"
