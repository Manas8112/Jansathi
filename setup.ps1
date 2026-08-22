# Setup script for JanSaathi Teammates

Write-Host "Setting up JanSaathi project..." -ForegroundColor Cyan

# 1. Fetch AI Models (Git LFS)
Write-Host "`n[1/4] Fetching trained AI models (this may take a minute)..." -ForegroundColor Yellow
try {
    git lfs install
    git lfs pull
    Write-Host "Models downloaded successfully!" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Git LFS not found or failed to pull. The local intent router may fall back to the cloud." -ForegroundColor Red
}

# 2. Install Frontend dependencies
Write-Host "`n[2/4] Installing Frontend Dependencies..." -ForegroundColor Yellow
cd frontend
npm install
cd ..

# 3. Install Backend dependencies
Write-Host "`n[3/4] Installing Backend Dependencies..." -ForegroundColor Yellow
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 4. Configure API Key
Write-Host "`n[4/4] Configuring Environment..." -ForegroundColor Yellow
Write-Host "JanSaathi uses the Groq API for its cloud LLM fallback."
$groqKey = Read-Host "Please enter your free Groq API key (or press Enter to skip)"
if ([string]::IsNullOrWhiteSpace($groqKey)) {
    Write-Host "Skipped. You will need to manually configure backend/.env later." -ForegroundColor Red
} else {
    $envContent = "GROQ_API_KEY=$groqKey"
    Set-Content -Path ".env" -Value $envContent -Encoding ASCII
    Write-Host "API Key successfully saved to backend/.env!" -ForegroundColor Green
}
cd ..

Write-Host "`n========================================="
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "Launching servers in new terminal windows..." -ForegroundColor Cyan
Write-Host "========================================="

# Launch servers
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; Write-Host 'Starting Frontend Server...' -ForegroundColor Cyan; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; Write-Host 'Starting Backend Server...' -ForegroundColor Cyan; .\.venv\Scripts\activate; uvicorn main:app --reload"
