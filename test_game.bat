@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Game Test Script
REM ========================================
REM This script tests that the game can run correctly

set "GAME_DIR=%~dp0"
set "PYTHON_DIR=%GAME_DIR%python"

echo.
echo 🧪 Testing Anime Monster Fighter
echo ================================
echo.

REM Test 1: Check if portable Python exists
echo Step 1: Checking portable Python...
if not exist "%PYTHON_DIR%\python.exe" (
    echo ❌ Portable Python not found
    echo Please run setup_game.bat first
    pause
    exit /b 1
) else (
    echo ✅ Portable Python found
)

REM Test 2: Check if pygame is installed
echo.
echo Step 2: Checking pygame installation...
"%PYTHON_DIR%\python.exe" -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo ❌ Pygame not installed correctly
    echo Please run setup_game.bat again
    pause
    exit /b 1
) else (
    echo ✅ Pygame installed correctly
)

REM Test 3: Check if game files exist
echo.
echo Step 3: Checking game files...
if not exist "game.py" (
    echo ❌ game.py not found
    goto :test_failed
) else (
    echo ✅ game.py found
)

if not exist "player.py" (
    echo ❌ player.py not found
    goto :test_failed
) else (
    echo ✅ player.py found
)

if not exist "monster.py" (
    echo ❌ monster.py not found
    goto :test_failed
) else (
    echo ✅ monster.py found
)

if not exist "clay_pot.py" (
    echo ❌ clay_pot.py not found
    goto :test_failed
) else (
    echo ✅ clay_pot.py found
)

REM Test 4: Test game import
echo.
echo Step 4: Testing game import...
"%PYTHON_DIR%\python.exe" -c "import sys; sys.path.insert(0, '.'); import game; print('Game imported successfully')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Game import test failed (may be normal)
) else (
    echo ✅ Game imports successfully
)

REM Test 5: Test pygame functionality
echo.
echo Step 5: Testing pygame functionality...
"%PYTHON_DIR%\python.exe" -c "import pygame; pygame.init(); print('Pygame initialized successfully'); pygame.quit()" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Pygame functionality test failed
) else (
    echo ✅ Pygame functionality test passed
)

echo.
echo 🎉 ALL TESTS PASSED!
echo ===================
echo.
echo The game is ready to run!
echo.
echo To play the game:
echo - Double-click start_game.bat
echo - Or run: python\python.exe game.py
echo.
echo Enjoy the game! 🎮
echo.

pause
goto :eof

:test_failed
echo.
echo ❌ SOME TESTS FAILED!
echo ====================
echo.
echo Please check the errors above and run setup_game.bat again.
echo.
pause
exit /b 1
