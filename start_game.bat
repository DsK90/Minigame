@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Anime Monster Fighter - Portable Game Launcher
REM ========================================
REM This script launches the game using the local portable Python installation

set "GAME_DIR=%~dp0"
set "PYTHON_DIR=%GAME_DIR%python"

echo.
echo 🎮 Anime Monster Fighter
echo =========================
echo Starting portable game...
echo.

REM Check if portable Python exists
if not exist "%PYTHON_DIR%\python.exe" (
    echo ❌ Portable Python not found.
    echo.
    echo Please run setup_game.bat first to create the portable installation.
    echo.
    echo This will download Python and install everything locally.
    echo.
    pause
    exit /b 1
)

REM Check if pygame is installed (in portable Python)
echo 🔍 Checking portable dependencies...
"%PYTHON_DIR%\python.exe" -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Pygame is not installed in portable Python.
    echo.
    echo Please run setup_game.bat again to install pygame.
    echo.
    pause
    exit /b 1
) else (
    echo ✅ All portable dependencies are ready
)

echo.
echo 🎯 Game Controls:
echo ================
echo • Arrow keys or WASD: Move around the dungeon
echo • Spacebar: Attack monsters and break clay pots
echo • R: Restart game (when game over)
echo.
echo 🎮 Game Tips:
echo =============
echo • Stay on the road tiles (gray paths) to move
echo • Attack monsters to gain points
echo • Break clay pots for lightning upgrades
echo • Find the yellow exit to advance to the next level
echo • Higher levels have more monsters and better rewards
echo.
echo Close the game window or press Ctrl+C to exit.
echo.

REM Set window title for better identification
title Anime Monster Fighter (Portable)

REM Launch the game using portable Python
"%PYTHON_DIR%\python.exe" game.py

REM Check if the game exited normally or crashed
if errorlevel 1 (
    echo.
    echo ❌ Game crashed or exited with an error.
    echo.
    echo Troubleshooting:
    echo • Make sure your graphics drivers are up to date
    echo • Try running as administrator
    echo • Check if you have the required permissions
    echo • Verify portable Python installation is complete
    echo.
    echo If the problem persists, please report the issue.
) else (
    echo.
    echo ✅ Game closed successfully.
    echo Thank you for playing! 🎮
)

echo.
pause
