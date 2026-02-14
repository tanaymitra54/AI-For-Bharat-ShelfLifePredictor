@echo off
REM install_python_winget.bat - Install Python 3.10 using Windows Package Manager

echo ========================================
echo Python 3.10 Installation via Winget
echo ========================================
echo.

REM Check if Python 3.9+ is already installed
echo [1/5] Checking for existing Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
    echo Found Python: %PYVER%
    echo.
    echo Python is already installed and ready!
    echo Skipping installation.
    echo.
    echo You can proceed to: setup_complete.bat
    pause
    exit /b 0
)

echo Python not found. Proceeding with installation...
echo.

REM Install Python using winget
echo [2/5] Installing Python 3.10 via Windows Package Manager...
echo This may take 2-3 minutes...
echo.

winget install Python.Python.3.10 --accept-package-agreements --accept-source-agreements
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Installation failed!
    echo Please try installing manually from:
    echo https://www.python.org/downloads/release/python-31013/
    echo.
    pause
    exit /b 1
)

echo.
echo Python 3.10 installed successfully!
echo.

REM Refresh environment variables
echo [3/5] Refreshing environment variables...
set PATH=C:\Users\soumy\AppData\Local\Programs\Python\Python310;C:\Users\soumy\AppData\Local\Programs\Python\Python310\Scripts;%PATH%
echo PATH updated.
echo.

REM Verify installation
echo [4/5] Verifying Python installation...
timeout /t 3 /nobreak >nul
python --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Python verification failed.
    echo You may need to restart your terminal for PATH changes to take effect.
) else (
    echo Python installation verified successfully!
)

REM Check pip
echo.
echo [5/5] Verifying pip installation...
python -m pip --version
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: pip verification failed.
) else (
    echo pip installation verified!
)
echo.

REM Upgrade pip
echo Upgrading pip to latest version...
python -m pip install --upgrade pip --quiet
if %ERRORLEVEL% EQU 0 (
    echo pip upgraded successfully!
)
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo IMPORTANT: Close this terminal and open a new one
echo for all PATH changes to take effect.
echo.
echo Next steps:
echo   1. Close and reopen this terminal
echo   2. Verify: python --version
echo   3. Run: setup_complete.bat
echo.
pause
