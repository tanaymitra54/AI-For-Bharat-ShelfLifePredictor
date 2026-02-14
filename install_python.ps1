# install_python.ps1 - Automated Python 3.10 Installation
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python 3.10 Automated Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python 3.10+ is already installed
Write-Host "[1/7] Checking existing Python installation..." -ForegroundColor Yellow
$pythonExists = Get-Command python -ErrorAction SilentlyContinue
if ($pythonExists) {
    $version = python --version 2>&1
    Write-Host "Python found: $version" -ForegroundColor Green
    
    # Check if version is 3.9+
    if ($version -match "Python 3\.(9|10|11|12)") {
        Write-Host "✓ Python 3.9+ already installed!" -ForegroundColor Green
        Write-Host "Skipping installation..." -ForegroundColor Yellow
        exit 0
    }
}

# Download Python 3.10 installer
Write-Host "[2/7] Downloading Python 3.10 installer..." -ForegroundColor Yellow
$downloadUrl = "https://www.python.org/ftp/python/3.10.13/python-3.10.13-amd64.exe"
$installerPath = "$env:TEMP\python-3.10.13-amd64.exe"

try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✓ Download completed successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Download failed: $_" -ForegroundColor Red
    exit 1
}

# Install Python with PATH enabled
Write-Host "[3/7] Installing Python 3.10..." -ForegroundColor Yellow
$installArgs = @(
    "/quiet",
    "InstallAllUsers=1",
    "PrependPath=1",
    "Include_test=0",
    "Include_doc=0",
    "Include_tcltk=0"
)

$process = Start-Process -FilePath $installerPath -ArgumentList $installArgs -Wait -PassThru

if ($process.ExitCode -eq 0) {
    Write-Host "✓ Python 3.10 installed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Installation failed with exit code: $($process.ExitCode)" -ForegroundColor Red
    exit 1
}

# Refresh environment variables
Write-Host "[4/7] Refreshing environment variables..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Verify installation
Write-Host "[5/7] Verifying Python installation..." -ForegroundColor Yellow
Start-Sleep -Seconds 3
$versionOutput = & python --version 2>&1

if ($versionOutput -match "Python 3\.10") {
    Write-Host "✓ Python $versionOutput verified" -ForegroundColor Green
} else {
    Write-Host "✗ Python verification failed" -ForegroundColor Red
    Write-Host "You may need to restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
}

# Check pip
Write-Host "[6/7] Verifying pip installation..." -ForegroundColor Yellow
$pipVersion = & python -m pip --version 2>&1
if ($pipVersion) {
    Write-Host "✓ $pipVersion" -ForegroundColor Green
} else {
    Write-Host "✗ pip verification failed" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "[7/7] Upgrading pip to latest version..." -ForegroundColor Yellow
& python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded successfully" -ForegroundColor Green

# Cleanup
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python 3.10 Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "1. Close and reopen your terminal" -ForegroundColor White
Write-Host "2. Verify installation: python --version" -ForegroundColor White
Write-Host "3. Continue with virtual environment setup" -ForegroundColor White
Write-Host ""
