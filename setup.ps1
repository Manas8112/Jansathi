# Setup script for JanSaathi Teammates

Write-Host "Setting up JanSaathi project..." -ForegroundColor Cyan

# 1. Fetch AI Models (Git LFS or Direct Download)
Write-Host "`n[1/4] Fetching trained AI models (this may take a minute)..." -ForegroundColor Yellow

$modelFile = "backend\models\intent_classifier\model.safetensors"
$modelIsMissing = $false
if (Test-Path $modelFile) {
    $fileInfo = Get-Item $modelFile
    if ($fileInfo.Length -lt 1MB) {
        $modelIsMissing = $true
    }
} else {
    $modelIsMissing = $true
}

if ($modelIsMissing) {
    try {
        git lfs install 2>$null
        git lfs pull 2>$null
    } catch {}
    
    # Recheck if it was pulled successfully
    $fileInfo = Get-Item $modelFile -ErrorAction SilentlyContinue
    if (-not $fileInfo -or $fileInfo.Length -lt 1MB) {
        Write-Host "Git LFS failed (likely because you downloaded the ZIP). Downloading model directly..." -ForegroundColor Cyan
        $url = "https://media.githubusercontent.com/media/Manas8112/Jansathi/main/backend/models/intent_classifier/model.safetensors"
        
        if (-not (Test-Path "backend\models\intent_classifier")) {
            New-Item -ItemType Directory -Force -Path "backend\models\intent_classifier" | Out-Null
        }
        
        Invoke-WebRequest -Uri $url -OutFile $modelFile
    }
    
    # Final check
    $fileInfo = Get-Item $modelFile -ErrorAction SilentlyContinue
    if ($fileInfo -and $fileInfo.Length -gt 1MB) {
        Write-Host "Models downloaded successfully!" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Failed to download the model. The local intent router may fall back to the cloud." -ForegroundColor Red
    }
} else {
    Write-Host "Model already exists and is the correct size!" -ForegroundColor Green
}

# 2. Install Frontend dependencies
Write-Host "`n[2/4] Installing Frontend Dependencies..." -ForegroundColor Yellow
cd frontend
npm install
cd ..

# 3. Install Backend dependencies
Write-Host "`n[3/4] Installing Backend Dependencies..." -ForegroundColor Yellow
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

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
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; Write-Host 'Starting Backend Server...' -ForegroundColor Cyan; .\.venv\Scripts\python.exe -m uvicorn main:app --reload"
