# AI Website Generator - Windows PowerShell Startup Script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AI Website Generator - Starting Application" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and add your API keys." -ForegroundColor Yellow
    exit 1
}

# Function to start backend
$backendScript = {
    Write-Host ""
    Write-Host "Starting Flask Backend Server..." -ForegroundColor Green
    Write-Host "Backend URL: http://localhost:5000" -ForegroundColor Cyan
    Write-Host ""
    python api.py
}

# Function to start frontend
$frontendScript = {
    Write-Host ""
    Write-Host "Starting React Frontend Server..." -ForegroundColor Green
    Write-Host "Frontend URL: http://localhost:3000" -ForegroundColor Cyan
    Write-Host ""
    Set-Location frontend
    npm run dev
}

# Ask user what to start
Write-Host "What would you like to start?" -ForegroundColor Yellow
Write-Host "1. Backend only (Flask API)" -ForegroundColor White
Write-Host "2. Frontend only (React App)" -ForegroundColor White
Write-Host "3. Both (Recommended - Opens 2 windows)" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "Starting Backend..." -ForegroundColor Green
        & $backendScript
    }
    "2" {
        Write-Host ""
        Write-Host "Starting Frontend..." -ForegroundColor Green
        & $frontendScript
    }
    "3" {
        Write-Host ""
        Write-Host "Starting both servers in separate windows..." -ForegroundColor Green
        Write-Host ""
        
        # Start backend in new window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { Write-Host 'Flask Backend Server' -ForegroundColor Cyan; python api.py }"
        
        Start-Sleep -Seconds 2
        
        # Start frontend in new window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { Write-Host 'React Frontend Server' -ForegroundColor Cyan; Set-Location frontend; npm run dev }"
        
        Write-Host "Both servers starting..." -ForegroundColor Green
        Write-Host ""
        Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
        Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Press any key to exit this window (servers will continue running)..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    default {
        Write-Host ""
        Write-Host "Invalid choice!" -ForegroundColor Red
        exit 1
    }
}
