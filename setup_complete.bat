@echo off
REM setup_complete.bat - Complete Automated Setup for Shelf Life Predictor
REM This script automates the entire setup process

echo.
echo ============================================
echo AI Food Shelf Life Predictor - Setup
echo ============================================
echo.
echo This script will guide you through:
echo   1. Installing Python 3.10
echo   2. Setting up virtual environment
echo   3. Installing dependencies
echo   4. Configuring API keys
echo   5. Training the ML model
echo   6. Starting the API server
echo.
echo Estimated time: 25-35 minutes
echo.
pause

REM Check if Python is already installed
echo.
echo ============================================
echo Step 1: Check Python Installation
echo ============================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
    echo Python found: %PYVER%
    echo.
    set PYTHON_INSTALLED=1
) else (
    echo Python not found.
    echo.
    echo Do you want to install Python 3.10 automatically?
    echo.
    choice /C YN /M "Install Python 3.10 now"

    if %ERRORLEVEL% EQU 1 (
        call install_python.bat
        if %ERRORLEVEL% NEQ 0 (
            echo.
            echo ERROR: Python installation failed!
            echo Please install Python manually and run this script again.
            pause
            exit /b 1
        )
        echo.
        echo IMPORTANT: Please close this terminal and open a new one
        echo to complete the Python installation.
        echo Then run this script again.
        echo.
        pause
        exit /b 0
    ) else (
        echo.
        echo Skipping Python installation.
        echo Please install Python 3.9+ manually and run this script again.
        echo.
        pause
        exit /b 1
    )
)

if "%PYTHON_INSTALLED%"=="1" (
    echo.
    echo Python is already installed and ready!
    echo.
)

REM Setup virtual environment
echo.
echo ============================================
echo Step 2: Setup Virtual Environment
echo ============================================
echo.

cd backend

if exist venv (
    echo Virtual environment already exists.
    choice /C YN /M "Recreate virtual environment"
    if %ERRORLEVEL% EQU 1 (
        rmdir /s /q venv
        echo Creating new virtual environment...
        python -m venv venv
        if %ERRORLEVEL% NEQ 0 (
            echo ERROR: Failed to create virtual environment!
            pause
            exit /b 1
        )
        echo Virtual environment created successfully.
    )
) else (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)

REM Install dependencies
echo.
echo ============================================
echo Step 3: Install Dependencies
echo ============================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python packages from requirements.txt...
echo This may take 3-5 minutes...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.

REM Configure API keys
echo.
echo ============================================
echo Step 4: Configure API Keys
echo ============================================
echo.
echo You can get FREE API keys for voice and chat features:
echo.
echo ElevenLabs (Voice): https://try.elevenlabs.io/a10z6n1mbyor
echo   - FREE tier: 10 minutes audio/month
echo.
echo OpenRouter (Chat): https://openrouter.ai
echo   - FREE tier: 50 requests/day
echo.
choice /C YN /M "Configure API keys now"

if %ERRORLEVEL% EQU 1 (
    cd ..
    call setup_env.bat
    cd backend
) else (
    echo.
    echo Skipping API key configuration.
    echo Note: Core prediction features work without API keys.
    echo You can configure them later by running: setup_env.bat
)

REM Train model
echo.
echo ============================================
echo Step 5: Train ML Model
echo ============================================
echo.

if exist models\shelf_life_predictor.pkl (
    echo Model already trained and saved.
    choice /C YN /M "Retrain model"
    if %ERRORLEVEL% EQU 2 (
        echo Skipping model training.
        goto :START_SERVER
    )
)

echo Training Random Forest model...
echo This will take 2-5 minutes...
python train.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Model training failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Model training completed successfully!
echo.

:START_SERVER
REM Start API server
echo.
echo ============================================
echo Step 6: Start API Server
echo ============================================
echo.
echo Ready to start the Flask API server.
echo.
echo The API will run on: http://localhost:5001
echo.
choice /C YN /M "Start API server now"

if %ERRORLEVEL% EQU 1 (
    echo.
    echo Starting Flask API server...
    echo Press CTRL+C to stop the server.
    echo.
    python api.py
) else (
    echo.
    echo Skipping server startup.
    echo.
    echo To start the server later:
    echo   1. Activate venv: venv\Scripts\activate.bat
    echo   2. Start server: python api.py
    echo.
)

REM Summary
echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo What's been done:
echo   [x] Python 3.10 installed/verified
echo   [x] Virtual environment created
echo   [x] Dependencies installed
echo   [x] API keys configured (optional)
echo   [x] ML model trained
echo   [x] API server ready
echo.
echo Available API endpoints:
echo   GET  http://localhost:5001/health
echo   POST http://localhost:5001/predict
echo   POST http://localhost:5001/explain
echo   POST http://localhost:5001/batch_predict
echo   POST http://localhost:5001/voice/explain
echo   POST http://localhost:5001/chat
echo.
echo Next steps:
echo   1. Test the API: curl http://localhost:5001/health
echo   2. Start frontend: cd ..\frontend ^&^& npm run dev
echo   3. Open browser: http://localhost:3000
echo.
echo For detailed documentation, see: SETUP_GUIDE.md
echo.
pause
