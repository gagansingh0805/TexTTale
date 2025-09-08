@echo off
echo ========================================
echo    AI Story Generator - Starting Up
echo ========================================
echo.

echo Checking for Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

echo.
echo Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo Installing backend dependencies...
cd ../backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo Checking for environment configuration...
if not exist ".env" (
    echo WARNING: No .env file found in backend directory
    echo Creating example .env file...
    echo # AI Story Generator Environment Configuration > .env
    echo # Copy this file and add your actual API keys >> .env
    echo. >> .env
    echo # Google Gemini API Key (Required for story generation) >> .env
    echo # Get your API key from: https://makersuite.google.com/app/apikey >> .env
    echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
    echo. >> .env
    echo # Hugging Face API Token (Optional - for image generation) >> .env
    echo # Get your token from: https://huggingface.co/settings/tokens >> .env
    echo HUGGINGFACE_API_TOKEN=your_hf_token_here >> .env
    echo.
    echo Please edit the .env file and add your API keys for full functionality.
    echo The app will work in fallback mode without API keys.
    echo.
)

cd ..
echo.
echo Starting both frontend and backend...
echo Frontend will be available at: http://localhost:3000
echo Backend will be available at: http://localhost:8001
echo.
echo Press Ctrl+C to stop both servers
echo.

npm run dev