@echo off
setlocal enabledelayedexpansion

REM ========================================
REM Anime Monster Fighter - Portable Installer
REM ========================================
REM This script creates a self-contained installation with portable Python
REM Works even without Python installed on the system

set "GAME_DIR=%~dp0"
set "PYTHON_DIR=%GAME_DIR%python"
set "PYTHON_VERSION=3.11.5"
set "PYTHON_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip"

echo.
echo 🎮 Anime Monster Fighter - Portable Installer
echo ============================================
echo.
echo This will create a completely self-contained installation.
echo Downloads portable Python and installs everything locally.
echo No system-wide changes required!
echo.

REM Check if we're running as administrator (better for some operations)
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as administrator - optimal for installation
) else (
    echo ⚠️  Running as regular user - should still work fine
)

echo.
echo 🔍 Step 1: Checking for existing portable Python...

REM Check if portable Python already exists
if exist "%PYTHON_DIR%\python.exe" (
    echo ✅ Portable Python already exists
    goto :check_pygame
)

echo 📥 Step 2: Downloading portable Python...

REM Check if we have curl or wget
curl --version >nul 2>&1
if errorlevel 1 (
    wget --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Neither curl nor wget found.
        echo.
        echo Please download portable Python manually:
        echo 1. Go to: %PYTHON_URL%
        echo 2. Download python-%PYTHON_VERSION%-embed-amd64.zip
        echo 3. Extract to: %PYTHON_DIR%
        echo 4. Run this script again
        echo.
        echo Press any key to open download page...
        pause >nul
        start %PYTHON_URL%
        exit /b 1
    ) else (
        set "DOWNLOAD_CMD=wget -O python-portable.zip %PYTHON_URL%"
    )
) else (
    set "DOWNLOAD_CMD=curl -L -o python-portable.zip %PYTHON_URL%"
)

REM Download portable Python
echo Downloading portable Python %PYTHON_VERSION%...
%DOWNLOAD_CMD%
if errorlevel 1 (
    echo ❌ Failed to download portable Python.
    echo.
    echo Please check your internet connection and try again.
    echo Or download manually from: %PYTHON_URL%
    echo.
    pause
    exit /b 1
)

REM Extract portable Python
echo 📦 Extracting portable Python...
if not exist "%PYTHON_DIR%" mkdir "%PYTHON_DIR%"
powershell -command "Expand-Archive -Path 'python-portable.zip' -DestinationPath '%PYTHON_DIR%' -Force"
del python-portable.zip

REM Verify extraction
if not exist "%PYTHON_DIR%\python.exe" (
    echo ❌ Failed to extract portable Python.
    echo.
    echo Please check if you have enough disk space and try again.
    echo.
    pause
    exit /b 1
)

echo ✅ Portable Python installed successfully

:check_pygame
echo.
echo 📦 Step 3: Installing pygame locally...

REM First, we need to install pip for the portable Python
echo Installing pip for portable Python...

REM Download get-pip.py if it doesn't exist
if not exist "get-pip.py" (
    echo Downloading get-pip.py...
    curl -L -o get-pip.py https://bootstrap.pypa.io/get-pip.py 2>nul
    if errorlevel 1 (
        wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py 2>nul
        if errorlevel 1 (
            echo ❌ Failed to download get-pip.py
            echo.
            echo Please check your internet connection and try again.
            echo.
            pause
            exit /b 1
        )
    )
)

REM Install pip using the portable Python
echo Running: "%PYTHON_DIR%\python.exe" get-pip.py --quiet
"%PYTHON_DIR%\python.exe" get-pip.py --quiet
if errorlevel 1 (
    echo ❌ Failed to install pip.
    echo.
    echo Trying without --quiet flag to see the error...
    "%PYTHON_DIR%\python.exe" get-pip.py
    if errorlevel 1 (
        echo ❌ Pip installation failed.
        echo.
        echo This is required for installing pygame.
        echo Please check your internet connection and try again.
        echo.
        echo If the problem persists, you may need to:
        echo 1. Check if you have enough disk space
        echo 2. Try running as administrator
        echo 3. Temporarily disable antivirus software
        echo.
        pause
        exit /b 1
    )
)

REM Clean up get-pip.py
del get-pip.py 2>nul

echo ✅ Pip installed successfully

REM Now install pygame using the portable Python
echo Installing pygame...

"%PYTHON_DIR%\python.exe" -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo ⚠️  Failed to upgrade pip, continuing with current version...
)

REM Try installing pygame with better error handling
"%PYTHON_DIR%\python.exe" -m pip install pygame --quiet
if errorlevel 1 (
    echo ❌ Failed to install pygame.
    echo.
    echo Trying alternative installation method...
    echo.

    REM Try installing without quiet flag to see the actual error
    echo Attempting pygame installation (showing output for debugging)...
    "%PYTHON_DIR%\python.exe" -m pip install pygame

    if errorlevel 1 (
        echo ❌ Pygame installation failed.
        echo.
        echo Common solutions:
        echo 1. Check your internet connection
        echo 2. Try running as administrator
        echo 3. Temporarily disable antivirus software
        echo 4. Make sure you have enough disk space
        echo.
        echo The game requires pygame to run. Without it, the game will not work.
        echo.
        echo If the problem persists, you can try:
        echo - Installing Python manually and running: pip install pygame
        echo - Or contact support with the error messages shown above
        echo.
        pause
        exit /b 1
    )
) else (
    echo ✅ Pygame installed successfully
)

REM Verify pygame installation
echo 🔍 Verifying pygame installation...
"%PYTHON_DIR%\python.exe" -c "import pygame; print('Pygame version:', pygame.version.ver)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Pygame import test failed, but installation reported success.
    echo The game may not work properly. Continuing anyway...
) else (
    echo ✅ Pygame verification successful
)

echo.
echo 🔗 Step 4: Creating desktop shortcuts...

REM Create desktop shortcut
set DESKTOP_DIR=%USERPROFILE%\Desktop
set SHORTCUT_NAME="Anime Monster Fighter.lnk"

REM Check if shortcut already exists
if exist "%DESKTOP_DIR%\%SHORTCUT_NAME%" (
    echo ℹ️  Desktop shortcut already exists
) else (
    REM Create VBS script to create shortcut
    echo Set oWS = WScript.CreateObject("WScript.Shell") > create_shortcut.vbs
    echo sLinkFile = "%DESKTOP_DIR%\%SHORTCUT_NAME%" >> create_shortcut.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> create_shortcut.vbs
    echo oLink.TargetPath = "%GAME_DIR%start_game.bat" >> create_shortcut.vbs
    echo oLink.WorkingDirectory = "%GAME_DIR%" >> create_shortcut.vbs
    echo oLink.IconLocation = "%GAME_DIR%icon.ico, 0" >> create_shortcut.vbs
    echo oLink.Description = "Anime Monster Fighter - Portable dungeon crawler game" >> create_shortcut.vbs
    echo oLink.Save >> create_shortcut.vbs

    cscript //nologo create_shortcut.vbs 2>nul
    del create_shortcut.vbs

    if exist "%DESKTOP_DIR%\%SHORTCUT_NAME%" (
        echo ✅ Desktop shortcut created
    ) else (
        echo ❌ Failed to create desktop shortcut
        echo    You can manually create a shortcut to start_game.bat
    )
)

echo.
echo 📁 Step 5: Creating Start Menu entry...

REM Create Start Menu shortcut
set START_MENU_DIR="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter"
if not exist %START_MENU_DIR% mkdir %START_MENU_DIR% 2>nul

set START_MENU_SHORTCUT="%START_MENU_DIR%\Anime Monster Fighter.lnk"

if exist %START_MENU_SHORTCUT% (
    echo ℹ️  Start Menu entry already exists
) else (
    echo Set oWS = WScript.CreateObject("WScript.Shell") > create_startmenu.vbs
    echo sLinkFile = %START_MENU_SHORTCUT% >> create_startmenu.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> create_startmenu.vbs
    echo oLink.TargetPath = "%GAME_DIR%start_game.bat" >> create_startmenu.vbs
    echo oLink.WorkingDirectory = "%GAME_DIR%" >> create_startmenu.vbs
    echo oLink.IconLocation = "%GAME_DIR%icon.ico, 0" >> create_startmenu.vbs
    echo oLink.Description = "Anime Monster Fighter - Portable dungeon crawler game" >> create_startmenu.vbs
    echo oLink.Save >> create_startmenu.vbs

    cscript //nologo create_startmenu.vbs 2>nul
    del create_startmenu.vbs

    if exist %START_MENU_SHORTCUT% (
        echo ✅ Start Menu entry created
    ) else (
        echo ❌ Failed to create Start Menu entry
    )
)

echo.
echo 🎯 Step 6: Creating portable uninstaller...

REM Create portable uninstaller script
echo @echo off > "%GAME_DIR%uninstall.bat"
echo setlocal enabledelayedexpansion >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo echo 🗑️  Uninstalling Anime Monster Fighter... >> "%GAME_DIR%uninstall.bat"
echo echo ======================================== >> "%GAME_DIR%uninstall.bat"
echo echo. >> "%GAME_DIR%uninstall.bat"
echo echo This will remove the portable installation. >> "%GAME_DIR%uninstall.bat"
echo echo. >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo REM Remove desktop shortcut >> "%GAME_DIR%uninstall.bat"
echo if exist "%%USERPROFILE%%\Desktop\Anime Monster Fighter.lnk" del "%%USERPROFILE%%\Desktop\Anime Monster Fighter.lnk" >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo REM Remove Start Menu entry >> "%GAME_DIR%uninstall.bat"
echo if exist "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter" rmdir /s /q "%%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter" >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo REM Remove portable Python and packages >> "%GAME_DIR%uninstall.bat"
echo if exist "python" rmdir /s /q "python" >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo REM Remove game files (optional - comment out if you want to keep them) >> "%GAME_DIR%uninstall.bat"
echo REM if exist "game.py" del "game.py" >> "%GAME_DIR%uninstall.bat"
echo REM if exist "player.py" del "player.py" >> "%GAME_DIR%uninstall.bat"
echo REM if exist "monster.py" del "monster.py" >> "%GAME_DIR%uninstall.bat"
echo REM if exist "clay_pot.py" del "clay_pot.py" >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo echo. >> "%GAME_DIR%uninstall.bat"
echo echo ✅ Portable uninstallation complete! >> "%GAME_DIR%uninstall.bat"
echo echo. >> "%GAME_DIR%uninstall.bat"
echo echo Note: Game source files were preserved. >> "%GAME_DIR%uninstall.bat"
echo echo Delete them manually if you want to remove everything. >> "%GAME_DIR%uninstall.bat"
echo. >> "%GAME_DIR%uninstall.bat"
echo pause >> "%GAME_DIR%uninstall.bat"

echo ✅ Portable uninstaller created

echo.
echo 🎉 Portable Installation Complete!
echo =================================
echo.
echo ✨ Everything is now self-contained in this folder:
echo    📁 %GAME_DIR%
echo.
echo 🎮 To play the game:
echo    • Double-click: "Anime Monster Fighter" desktop shortcut
echo    • Or run: start_game.bat (from this folder)
echo.
echo 🔧 What's installed locally:
echo    • Portable Python %PYTHON_VERSION% (%PYTHON_DIR%)
echo    • Pygame library (installed locally)
echo    • All game files (completely portable)
echo.
echo 🎯 Game Controls:
echo    • Arrow keys or WASD: Move around the dungeon
echo    • Spacebar: Attack monsters and break clay pots
echo    • R: Restart game (when game over)
echo.
echo 🗑️  To uninstall:
echo     • Run: uninstall.bat (from this folder)
echo.
echo 📝 Key Features:
echo    • ✅ Works without system Python installation
echo    • ✅ No administrator privileges required
echo    • ✅ Everything contained in game folder (~50MB total)
echo    • ✅ Single pygame dependency only
echo    • ✅ Portable - copy folder to any Windows PC
echo.
echo Enjoy the game! 🎮
echo.

pause
