@echo off
REM AgentMesh Frontend Startup Script for Windows

echo.
echo ====================================================
echo   AgentMesh Frontend - Startup Script
echo ====================================================
echo.

REM Check if we're in the right directory
if not exist "AgentMesh\UI\frontend\package.json" (
    echo ERROR: Frontend files not found!
    echo Please run this script from the project root directory.
    echo Expected: D:\project\AgentMesh\
    pause
    exit /b 1
)

echo [1/3] Checking Node.js installation...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    echo Download: https://nodejs.org/en/download/
    pause
    exit /b 1
)

echo [2/3] Checking npm packages...
cd /d AgentMesh\UI\frontend
if not exist "node_modules" (
    echo Installing npm packages (this may take a minute)...
    call npm install
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install npm packages
        pause
        exit /b 1
    )
)

if not exist "public\styles.css" (
    echo Building Tailwind CSS...
    call npm run build
)

echo [3/3] Starting frontend server...
echo.
echo Frontend Server:
echo   URL: http://localhost:8080
echo   Integration Dashboard: http://localhost:8080/integration.html
echo   Press Ctrl+C to stop
echo.
echo TIP: Open frontend in your browser while backend is running (http://localhost:5000)
echo.

call npm run dev

pause
