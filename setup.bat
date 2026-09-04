@echo off
echo ====================================
echo    SWARAJ Setup Script
echo ====================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/5] Installing Python dependencies...
pip install SpeechRecognition pyttsx3 python-dotenv requests wikipedia pyaudio

echo [3/5] Installing PyAudio...
pip install pipwin 2>nul
pipwin install pyaudio 2>nul
pip install pyaudio 2>nul

echo [4/5] Copying .env template...
if not exist .env (
    copy .env.example .env
    echo Created .env file.
) else (
    echo .env file already exists.
)

echo [5/5] Checking Ollama...
ollama --version 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ===========================================
    echo   OLLAMA NOT FOUND - Please install it:
    echo   https://ollama.com/download
    echo.
    echo   After installing, run:
    echo     ollama serve
    echo     ollama pull llama3.2
    echo ===========================================
) else (
    echo Ollama found! Checking if running...
    ollama list 2>nul
    if %errorlevel% neq 0 (
        echo Please run: ollama serve
    )
)

echo.
echo ====================================
echo    Setup Complete!
echo ====================================
echo.
echo Quick start:
echo   1. Install Ollama: https://ollama.com/download
echo   2. Run: ollama serve
echo   3. Run: ollama pull llama3.2
echo   4. Run: python swaraj.py --text
echo.
pause
