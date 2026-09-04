@echo off
title SWARAJ - Voice Assistant
color 0A
echo.
echo  ███████╗██╗   ██╗██████╗ ██╗   ██╗██████╗ ███████╗ █████╗ ███╗   ██╗
echo  ██╔════╝╚██╗ ██╔╝██╔══██╗██║   ██║██╔══██╗██╔════╝██╔══██╗████╗  ██║
echo  ███████╗ ╚████╔╝ ██████╔╝██║   ██║██████╔╝█████╗  ███████║██╔██╗ ██║
echo  ╚════██║  ╚██╔╝  ██╔══██╗██║   ██║██╔═══╝ ██╔══╝  ██╔══██║██║╚██╗██║
echo  ███████║   ██║   ██████╔╝╚██████╔╝██║     ███████╗██║  ██║██║ ╚████║
echo  ╚══════╝   ╚═╝   ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
echo.
echo  [1] Text Mode (Type commands)
echo  [2] Voice Mode (Say "Hey Swaraj")
echo  [3] Voice Mode (Always listening)
echo  [4] GUI Mode (Siri-like interface)
echo  [5] Setup (First time / retrain)
echo  [6] Hindi Mode
echo  [7] Marathi Mode
echo  [8] Exit
echo.
set /p choice="Choose option (1-8): "

if "%choice%"=="1" (
    echo.
    echo Starting Text Mode...
    python swaraj.py --text
) else if "%choice%"=="2" (
    echo.
    echo Starting Voice Mode (say "Hey Swaraj" to activate)...
    python swaraj.py
) else if "%choice%"=="3" (
    echo.
    echo Starting Voice Mode (always listening)...
    python swaraj.py --voice
) else if "%choice%"=="4" (
    echo.
    echo Starting GUI...
    python swaraj.py --ui
) else if "%choice%"=="5" (
    echo.
    python swaraj.py --setup
) else if "%choice%"=="6" (
    echo.
    echo Starting Hindi Mode...
    python swaraj.py --text --lang hindi
) else if "%choice%"=="7" (
    echo.
    echo Starting Marathi Mode...
    python swaraj.py --text --lang marathi
) else if "%choice%"=="8" (
    echo Goodbye!
    exit
) else (
    echo Invalid choice. Starting Text Mode...
    python swaraj.py --text
)
