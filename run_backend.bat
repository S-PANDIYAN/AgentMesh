@echo off
REM AgentMesh Backend Startup Script for Windows

echo.
echo ====================================================
echo   AgentMesh Backend - Startup Script
echo ====================================================
echo.

REM Check if we're in the right directory
if not exist "AgentMesh\backend\rest_api_v2.py" (
    echo ERROR: Backend files not found!
    echo Please run this script from the project root directory.
    echo Expected: D:\project\AgentMesh\
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [2/3] Checking required packages...
python -c "import flask; import sqlalchemy; import jwt" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Required packages not installed
    echo Installing now...
    pip install -q flask flask-cors pyjwt bcrypt sqlalchemy psycopg2-binary reportlab jinja2 pandas
)

echo [3/3] Starting backend server...
echo.
echo Backend Server:
echo   URL: http://localhost:5000
echo   Press Ctrl+C to stop
echo.

cd /d AgentMesh
python -m backend.rest_api_v2 --debug --host 0.0.0.0 --port 5000

pause
