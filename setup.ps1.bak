[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Setup script for JanSaathi Teammates

$baseDir = $PSScriptRoot

Write-Host "Setting up JanSaathi project..." -ForegroundColor Cyan

# 1. Fetch AI Models (Git LFS or Direct Download)
Write-Host "`n[1/4] Fetching trained AI models (this may take a minute)..." -ForegroundColor Yellow

$modelFile = "$baseDir\backend\models\intent_classifier\model.safetensors"
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

    # Recheck after LFS pull
    $fileInfo = Get-Item $modelFile -ErrorAction SilentlyContinue
    if (-not $fileInfo -or $fileInfo.Length -lt 1MB) {
        Write-Host "Git LFS failed (likely because you downloaded the ZIP). Downloading model directly..." -ForegroundColor Cyan
        $url = "https://media.githubusercontent.com/media/Manas8112/Jansathi/main/backend/models/intent_classifier/model.safetensors"

        if (-not (Test-Path "$baseDir\backend\models\intent_classifier")) {
            New-Item -ItemType Directory -Force -Path "$baseDir\backend\models\intent_classifier" | Out-Null
        }

        Invoke-WebRequest -Uri $url -OutFile $modelFile
    }

    # Final size check
    $fileInfo = Get-Item $modelFile -ErrorAction SilentlyContinue
    if ($fileInfo -and $fileInfo.Length -gt 1MB) {
        Write-Host "Models downloaded successfully!" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Failed to download the model. The intent router will fall back to Groq LLM automatically." -ForegroundColor Red
    }
} else {
    Write-Host "Model already exists and is the correct size — skipping download." -ForegroundColor Green
}

# 2. Install Frontend dependencies
Write-Host "`n[2/4] Installing Frontend Dependencies..." -ForegroundColor Yellow
Set-Location "$baseDir\frontend"
npm install
Set-Location $baseDir

# 3. Install Backend dependencies
Write-Host "`n[3/4] Installing Backend Dependencies..." -ForegroundColor Yellow
Set-Location "$baseDir\backend"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Set-Location $baseDir

# 4. Configure API Key
Write-Host "`n[4/4] Configuring Environment..." -ForegroundColor Yellow
Write-Host "JanSaathi uses the Groq API for its cloud LLM. Get a free key at https://console.groq.com"
$groqKey = Read-Host "Please enter your Groq API key (or press Enter to skip)"

if ([string]::IsNullOrWhiteSpace($groqKey)) {
    Write-Host "Skipped. You will need to manually add GROQ_API_KEY to backend/.env later." -ForegroundColor Red
} else {
    $envContent = "GROQ_API_KEY=$groqKey"
    Set-Content -Path "$baseDir\backend\.env" -Value $envContent -Encoding UTF8
    Write-Host "API Key saved to backend/.env!" -ForegroundColor Green
}

Write-Host "`n========================================="
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "Launching servers in new terminal windows..." -ForegroundColor Cyan
Write-Host "========================================="

# Launch both servers in separate windows
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$baseDir\frontend`"; Write-Host 'Starting Frontend Server...' -ForegroundColor Cyan; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$baseDir\backend`"; Write-Host 'Starting Backend Server...' -ForegroundColor Cyan; .\.venv\Scripts\python.exe -m uvicorn main:app --reload"
