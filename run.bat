@echo off
echo ========================================================
echo   Starting Ansh Rastogi Portfolio & Groq RAG Engine
echo ========================================================
echo.

REM 1. Start Groq RAG Backend API on Port 8000 in a new window
start "Groq RAG API Server (Port 8000)" cmd /k "python rag_pipeline.py --serve --port 8000"

REM 2. Start Portfolio Web Server on Port 3000 in a new window
start "Web Portfolio Server (Port 3000)" cmd /k "python -m http.server 3000"

echo [OK] Both servers launched!
echo Opening http://localhost:3000 in your browser...
timeout /t 2 >nul
start http://localhost:3000

echo.
echo Portfolio URL: http://localhost:3000
echo RAG API URL:   http://localhost:8000
echo ========================================================

