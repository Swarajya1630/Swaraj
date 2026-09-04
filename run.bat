@echo off
echo Starting SWARAJ...
echo.
echo Choose mode:
echo   1. Voice mode with wake word (say "Hey Swaraj")
echo   2. Voice mode (continuous listening)
echo   3. Text mode (type commands)
echo.
echo Choose language:
echo   [E] English  [H] Hindi  [M] Marathi
echo.
set /p mode="Enter mode (1/2/3): "
set /p lang="Enter language (E/H/M): "

if "%lang%"=="H" (
    set langname=hindi
) else if "%lang%"=="M" (
    set langname=marathi
) else (
    set langname=english
)

if "%mode%"=="1" (
    python swaraj.py --lang %langname%
) else if "%mode%"=="2" (
    python swaraj.py --no-wake --lang %langname%
) else if "%mode%"=="3" (
    python swaraj.py --text --lang %langname%
) else (
    echo Invalid choice. Starting text mode in English...
    python swaraj.py --text --lang english
)
