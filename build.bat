@echo off
title SWARAJ - Build
color 0B

echo.
echo  ================================
echo       BUILD SWARAJ
echo  ================================
echo.

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo Python not found! Install Python 3.10+
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller opencv-python

echo.
echo [3/4] Building executable...
pyinstaller Swaraj.spec --clean --noconfirm

echo.
echo [4/4] Build complete!
echo.
echo  Executable: dist\Swaraj\Swaraj.exe
echo  Folder: dist\Swaraj\
echo.
echo  You can copy the entire dist\Swaraj folder
echo  to any Windows computer and run Swaraj.exe
echo.

pause
