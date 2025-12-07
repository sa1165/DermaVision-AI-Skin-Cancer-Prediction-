# PowerShell script to prepare and deploy to Netlify
# Usage: .\deploy-netlify.ps1

Write-Host "=== DermaVision Netlify Deployment Helper ===" -ForegroundColor Cyan
Write-Host ""

# Check if frontend folder exists
if (-not (Test-Path "frontend")) {
    Write-Host "Error: frontend folder not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Step 1: Creating deployment package..." -ForegroundColor Yellow

# Create a zip file of the frontend
$zipPath = "frontend-deploy.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path "frontend\*" -DestinationPath $zipPath -Force

if (Test-Path $zipPath) {
    Write-Host "Package created: $zipPath" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://app.netlify.com/drop" -ForegroundColor White
    Write-Host "2. Drag and drop: $zipPath" -ForegroundColor White
    Write-Host "3. Your site will be live in seconds!" -ForegroundColor White
    Write-Host ""
    Write-Host "Remember to update the backend URL in frontend/script.js" -ForegroundColor Yellow
    Write-Host ""
    
    # Ask if user wants to open Netlify
    $response = Read-Host "Open Netlify deploy page? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Start-Process "https://app.netlify.com/drop"
    }
} else {
    Write-Host "Error: Failed to create package" -ForegroundColor Red
    exit 1
}
