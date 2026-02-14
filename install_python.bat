@echo off
REM install_python.bat - Automated Python 3.10 Installation for Windows
echo ========================================
echo Python 3.10 Automated Installation
echo ========================================
echo.

REM Check if Python 3.9+ is already installed
echo [1/6] Checking for existing Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Python found, checking version...
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
    echo Found Python: %PYVER%
    echo.
    echo Python is already installed! Skipping installation.
    echo You can proceed to Step 3: Setup Virtual Environment
    pause
    exit /b 0
)

echo Python not found or version too old. Proceeding with installation...
echo.

REM Download Python 3.10 installer
echo [2/6] Downloading Python 3.10.13 installer...
set DOWNLOAD_URL=https://www.python.org/ftp/python/3.10.13/python-3.10.13-amd64.exe
set INSTALLER_PATH=%TEMP%\python-3.10.13-amd64.exe

powershell -Command "Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%INSTALLER_PATH%' -UseBasicParsing"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Download failed!
    pause
    exit /b 1
)
echo Download completed successfully.
echo.

REM Install Python
echo [3/6] Installing Python 3.10.13...
echo This may take a few minutes...
"%INSTALLER_PATH%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_doc=0 Include_tcltk=0
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Installation failed!
    pause
    exit /b 1
)
echo Python installed successfully.
echo.

REM Refresh PATH
echo [4/6] Refreshing environment variables...
set PATH=C:\Program Files\Python310;C:\Program Files\Python310\Scripts;%PATH%
echo PATH updated.
echo.

REM Verify installation
echo [5/6] Verifying Python installation...
timeout /t 3 /nobreak >nul
python --version
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Python verification failed.
    echo You may need to restart your terminal for PATH changes to take effect.
) else (
    echo Python installation verified successfully!
)
echo.

REM Check pip
echo [6/6] Verifying pip installation...
python -m pip --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip verification failed!
    pause
    exit /b 1
) else (
    echo pip installation verified!
)
echo.

REM Cleanup
del "%INSTALLER_PATH%" 2>nul

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo IMPORTANT: Close this terminal and open a new one
echo for PATH changes to take effect.
echo.
echo Next steps:
echo 1. Close and reopen this terminal
echo 2. Verify: python --version
echo 3. Continue to Step 3: Setup Virtual Environment
echo.
pause
