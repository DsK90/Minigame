@echo off
echo 🎮 Starting MiniGame...
echo =====================
echo.

REM Check if pygame is installed
python -c "import pygame" 2>nul
if errorlevel 1 (
    echo ❌ Pygame is not installed.
    echo Installing pygame...
    echo.
    pip install pygame
    if errorlevel 1 (
        echo ❌ Failed to install pygame. Please install it manually:
        echo pip install pygame
        pause
        exit /b 1
    )
)

echo ✅ Starting game...
echo.
echo Controls:
echo - Arrow keys: Move
echo - Spacebar: Attack
echo - R: Restart (when game over)
echo.
echo Close the game window to exit.
echo.

python game.py

echo.
echo Game closed.
pause
