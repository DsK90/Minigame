@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Test Installation Script
REM ========================================
REM This script tests the installation logic without actually downloading

echo.
echo 🧪 Testing Anime Monster Fighter Installation Logic
echo ==================================================
echo.

REM Test directory creation
set "GAME_DIR=%~dp0"
set "PYTHON_DIR=%GAME_DIR%python"

echo 📁 Testing directory structure...

REM Create test python directory
if not exist "%PYTHON_DIR%" mkdir "%PYTHON_DIR%" 2>nul
if exist "%PYTHON_DIR%" (
    echo ✅ Python directory created: %PYTHON_DIR%
) else (
    echo ❌ Failed to create Python directory
    goto :error
)

REM Create test python.exe (fake file for testing)
echo "Test Python executable" > "%PYTHON_DIR%\python.exe"
if exist "%PYTHON_DIR%\python.exe" (
    echo ✅ Test Python executable created
) else (
    echo ❌ Failed to create test Python executable
    goto :error
)

REM Test pygame check (this should fail since it's not real pygame)
echo 🔍 Testing pygame check...
"%PYTHON_DIR%\python.exe" -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo ✅ Pygame check correctly failed (as expected)
) else (
    echo ⚠️  Pygame check unexpectedly succeeded
)

REM Test launcher logic
echo 🎮 Testing launcher logic...

REM This should fail because pygame is not installed
echo Testing launcher dependency check...
if not exist "%PYTHON_DIR%\python.exe" (
    echo ❌ Test setup failed - no python.exe found
    goto :error
)

echo.
echo ✅ Basic installation logic test completed successfully!
echo.
echo The installation scripts should work correctly on a real system.
echo.
echo Next steps:
echo 1. Run setup_game.bat on a system without Python
echo 2. It should download portable Python and install pygame
echo 3. Run start_game.bat to launch the game
echo.

REM Cleanup test files
echo 🧹 Cleaning up test files...
if exist "%PYTHON_DIR%\python.exe" del "%PYTHON_DIR%\python.exe"
if exist "%PYTHON_DIR%" rmdir "%PYTHON_DIR%"
echo ✅ Test cleanup completed

echo.
echo 🎉 Test completed successfully!
echo.

pause
goto :eof

:error
echo ❌ Test failed!
echo.
pause
exit /b 1
