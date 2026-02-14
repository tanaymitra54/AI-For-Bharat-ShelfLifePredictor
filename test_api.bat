@echo off
REM test_api.bat - Test all API endpoints

echo.
echo ============================================
echo API Testing Script
echo ============================================
echo.
echo This script will test all API endpoints.
echo Make sure the API server is running first!
echo.

choice /C YN /M "Is API server running on localhost:5001"

if %ERRORLEVEL% EQU 2 (
    echo.
    echo Please start the API server first:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   python api.py
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Test 1: Health Check
echo ============================================
echo.
curl -s http://localhost:5001/health
echo.
echo.

echo ============================================
echo Test 2: Basic Prediction (Dairy, Normal Conditions)
echo ============================================
echo.
curl -s -X POST http://localhost:5001/predict -H "Content-Type: application/json" -d "{\"food_type\":\"dairy\",\"temperature\":4,\"humidity\":65,\"storage_type\":\"refrigerator\",\"days_stored\":2}"
echo.
echo.

echo ============================================
echo Test 3: Extreme Conditions (Meat, Danger Zone)
echo ============================================
echo.
curl -s -X POST http://localhost:5001/predict -H "Content-Type: application/json" -d "{\"food_type\":\"meat\",\"temperature\":15,\"humidity\":85,\"storage_type\":\"refrigerator\",\"days_stored\":4}"
echo.
echo.

echo ============================================
echo Test 4: Explanation Endpoint
echo ============================================
echo.
curl -s -X POST http://localhost:5001/explain -H "Content-Type: application/json" -d "{\"food_type\":\"fruits\",\"temperature\":4,\"humidity\":80,\"storage_type\":\"refrigerator\",\"days_stored\":6}"
echo.
echo.

echo ============================================
echo Test 5: Batch Predictions
echo ============================================
echo.
curl -s -X POST http://localhost:5001/batch_predict -H "Content-Type: application/json" -d "{\"items\":[{\"food_type\":\"dairy\",\"temperature\":4,\"humidity\":65,\"storage_type\":\"refrigerator\",\"days_stored\":2},{\"food_type\":\"meat\",\"temperature\":4,\"humidity\":60,\"storage_type\":\"refrigerator\",\"days_stored\":3}]}"
echo.
echo.

echo ============================================
echo Test 6: Storage Advice (Chat)
echo ============================================
echo.
echo Note: This test requires OpenRouter API key.
echo.
curl -s -X POST http://localhost:5001/chat/storage_advice -H "Content-Type: application/json" -d "{\"food_type\":\"dairy\",\"storage_conditions\":{\"storage_type\":\"refrigerator\",\"temperature\":4,\"humidity\":65}}"
echo.
echo.

echo.
echo ============================================
echo All Tests Completed!
echo ============================================
echo.
echo If you see valid JSON responses above, the API is working correctly!
echo.
pause
