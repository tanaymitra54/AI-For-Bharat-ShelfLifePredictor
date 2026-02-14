@echo off
REM setup_env.bat - Setup .env file with API keys (Windows)

cd config

REM Copy .env.example to .env
if not exist .env.example (
    echo ERROR: .env.example not found!
    pause
    exit /b 1
)

copy .env.example .env >nul
echo .env file created from template.
echo.

echo ========================================
echo Configuration Setup
echo ========================================
echo.
echo Please enter your API keys (or press Enter to skip):
echo.

REM Prompt for ElevenLabs API key
set /p ELEVENLABS_KEY="ElevenLabs API Key: "

REM Prompt for OpenRouter API key
set /p OPENROUTER_KEY="OpenRouter API Key: "

REM Update .env file
if not "%ELEVENLABS_KEY%"=="" (
    powershell -Command "(Get-Content .env) -replace 'your_elevenlabs_api_key', '%ELEVENLABS_KEY%' | Set-Content .env"
    echo ElevenLabs API key configured.
) else (
    echo ElevenLabs API key skipped (optional feature).
)

if not "%OPENROUTER_KEY%"=="" (
    powershell -Command "(Get-Content .env) -replace 'your_openrouter_api_key', '%OPENROUTER_KEY%' | Set-Content .env"
    echo OpenRouter API key configured.
) else (
    echo OpenRouter API key skipped (optional feature).
)

echo.
echo ========================================
echo Configuration Complete!
echo ========================================
echo.
echo Note: Core prediction features work without API keys.
echo API keys are only needed for voice and chat features.
echo.
echo Your .env file is ready at: config\.env
echo.
pause
