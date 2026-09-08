@echo off
title SWARAJ - AI Assistant
color 0B

echo.
echo  ================================
echo       S W A R A J
echo   AI Voice Assistant
echo  ================================
echo.
echo  [1] Start SWARAJ (Background)
echo  [2] Start SWARAJ (Text Mode)
echo  [3] Start SWARAJ (UI Mode)
echo  [4] Setup / Configure
echo  [5] View Logs
echo  [6] Exit
echo.
set /p choice="Select option: "

if "%choice%"=="1" goto background
if "%choice%"=="2" goto text
if "%choice%"=="3" goto ui
if "%choice%"=="4" goto setup
if "%choice%"=="5" goto logs
if "%choice%"=="6" goto exit

echo Invalid option. Try again.
pause
goto start

:background
echo.
echo Starting SWARAJ in background mode...
python app/main.py
goto end

:text
echo.
echo Starting SWARAJ in text mode...
python app/main.py --text
goto end

:ui
echo.
echo Starting SWARAJ in UI mode...
python app/main.py --ui
goto end

:setup
echo.
echo Starting SWARAJ setup...
python app/main.py --setup
goto end

:logs
echo.
echo Opening logs folder...
explorer logs
goto start

:exit
echo.
echo Goodbye!
exit /b

:end
pause
