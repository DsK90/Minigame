@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Installation Verification Script
REM ========================================
REM This script helps verify that the portable installation is working correctly

set "GAME_DIR=%~dp0"
set "PYTHON_DIR=%GAME_DIR%python"

echo.
echo 🔍 Anime Monster Fighter - Installation Verification
echo ==================================================
echo.

REM Check if portable Python exists
echo Step 1: Checking portable Python installation...
if not exist "%PYTHON_DIR%\python.exe" (
    echo ❌ Portable Python not found at: %PYTHON_DIR%\python.exe
    echo.
    echo Please run setup_game.bat first to install the portable Python.
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Portable Python found
)

REM Check Python version
echo.
echo Step 2: Checking Python version...
"%PYTHON_DIR%\python.exe" --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Failed to run portable Python
    echo.
    echo The portable Python installation may be corrupted.
    echo Try running setup_game.bat again.
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('"%PYTHON_DIR%\python.exe" --version 2^>nul') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! is working
)

REM Check if pip is available
echo.
echo Step 3: Checking pip installation...
"%PYTHON_DIR%\python.exe" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pip is not available
    echo.
    echo This usually means pip installation failed.
    echo Try running setup_game.bat again.
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('"%PYTHON_DIR%\python.exe" -m pip --version 2^>nul') do set PIP_VERSION=%%i
    echo ✅ Pip !PIP_VERSION! is available
)

REM Check if pygame is installed
echo.
echo Step 4: Checking pygame installation...
"%PYTHON_DIR%\python.exe" -c "import pygame; print('Pygame version:', pygame.version.ver)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Pygame is not properly installed
    echo.
    echo This means the pygame installation failed or is incomplete.
    echo Try running setup_game.bat again.
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=3" %%i in ('"%PYTHON_DIR%\python.exe" -c "import pygame; print(pygame.version.ver)" 2^>nul') do set PYGAME_VERSION=%%i
    echo ✅ Pygame !PYGAME_VERSION! is properly installed
)

REM Check if game files exist
echo.
echo Step 5: Checking game files...
if not exist "game.py" (
    echo ❌ game.py not found
    goto :verification_failed
) else (
    echo ✅ game.py found
)

if not exist "player.py" (
    echo ❌ player.py not found
    goto :verification_failed
) else (
    echo ✅ player.py found
)

if not exist "monster.py" (
    echo ❌ monster.py not found
    goto :verification_failed
) else (
    echo ✅ monster.py found
)

if not exist "clay_pot.py" (
    echo ❌ clay_pot.py not found
    goto :verification_failed
) else (
    echo ✅ clay_pot.py found
)

REM Try to run a quick game test (without GUI)
echo.
echo Step 6: Testing game import...
"%PYTHON_DIR%\python.exe" -c "import game; print('Game module imports successfully')" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Game module has import issues (this may be normal)
) else (
    echo ✅ Game module imports successfully
)

echo.
echo 🎉 VERIFICATION COMPLETE!
echo ========================
echo.
echo ✅ All critical components are properly installed!
echo.
echo Your portable installation is ready to use.
echo You can now run the game using:
echo   - Desktop shortcut: "Anime Monster Fighter"
echo   - Command: start_game.bat
echo.
echo If you encounter any issues while playing the game,
echo check the troubleshooting section in README.md
echo.

pause
goto :eof

:verification_failed
echo.
echo ❌ VERIFICATION FAILED!
echo ======================
echo.
echo Some required files are missing.
echo Please ensure all game files are present and try again.
echo.
echo If the problem persists, run setup_game.bat to reinstall.
echo.
pause
exit /b 1
