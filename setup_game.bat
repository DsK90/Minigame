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

REM Download portable Python using PowerShell
echo Downloading portable Python %PYTHON_VERSION%...
powershell -command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile 'python-portable.zip'" 2>nul
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
powershell -command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('python-portable.zip', '%PYTHON_DIR%')"
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

REM Configure portable Python to find installed packages
echo Configuring portable Python...

REM Create necessary directories first
if not exist "%PYTHON_DIR%\Lib" mkdir "%PYTHON_DIR%\Lib"
if not exist "%PYTHON_DIR%\Lib\site-packages" mkdir "%PYTHON_DIR%\Lib\site-packages"
if not exist "%PYTHON_DIR%\Scripts" mkdir "%PYTHON_DIR%\Scripts"

REM Create or fix the _pth file
echo Creating python311._pth configuration file...
echo python311.zip> "%PYTHON_DIR%\python311._pth"
echo .>> "%PYTHON_DIR%\python311._pth"
echo Lib\site-packages>> "%PYTHON_DIR%\python311._pth"
echo.>> "%PYTHON_DIR%\python311._pth"
echo # Enable site module for package discovery>> "%PYTHON_DIR%\python311._pth"
echo import site>> "%PYTHON_DIR%\python311._pth"

echo ✅ Portable Python installed successfully

REM Verify Python configuration
echo Testing Python configuration...
call "%PYTHON_DIR%\python.exe" -c "import sys; print('Python path includes site-packages:', 'site-packages' in str(sys.path))" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Python configuration may not be optimal, but continuing...
) else (
    echo ✅ Python configuration verified
)

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
        echo ❌ curl failed, trying wget...
        wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py 2>nul
        if errorlevel 1 (
            echo ❌ Both curl and wget failed to download get-pip.py
            echo.
            echo Please check your internet connection and try again.
            echo You can also manually download get-pip.py from:
            echo https://bootstrap.pypa.io/get-pip.py
            echo and place it in the game folder, then run this script again.
            echo.
            pause
            exit /b 1
        )
    )
    echo ✅ Downloaded get-pip.py successfully
)

REM Install pip using the portable Python
echo Installing pip...
call "%PYTHON_DIR%\python.exe" get-pip.py --quiet --no-warn-script-location
if errorlevel 1 (
    echo ❌ Failed to install pip with --quiet flag.
    echo.
    echo Trying without --quiet flag to see the error...
    call "%PYTHON_DIR%\python.exe" get-pip.py --no-warn-script-location
    if errorlevel 1 (
        echo ❌ Pip installation failed completely.
        echo.
        echo This is required for installing pygame.
        echo Please check your internet connection and try again.
        echo.
        echo Troubleshooting steps:
        echo 1. Check if you have enough disk space (need ~50MB free)
        echo 2. Try running as administrator
        echo 3. Temporarily disable antivirus software
        echo 4. Check firewall settings
        echo.
        echo If the problem persists, you may need to:
        echo   - Delete the python folder and try again
        echo   - Or install Python manually and run: python -m pip install pygame
        echo.
        pause
        exit /b 1
    )
)

REM Clean up get-pip.py
del get-pip.py 2>nul

echo ✅ Pip installed successfully

REM Verify pip installation
echo Verifying pip installation...
call "%PYTHON_DIR%\python.exe" -m pip --version
if errorlevel 1 (
    echo ❌ Pip verification failed!
    echo.
    echo Pip was installed but is not working properly.
    echo This might indicate a corrupted installation.
    echo Try deleting the python folder and running setup again.
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Pip verification successful
)

REM Now install pygame using the portable Python
echo Installing pygame...

call "%PYTHON_DIR%\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Failed to upgrade pip, continuing with current version...
)

REM Install pygame
echo Installing pygame...

REM Check if pygame is already installed
call "%PYTHON_DIR%\python.exe" -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo Pygame not found, installing...

    REM Install pygame (use simple command that works manually)
    call "%PYTHON_DIR%\python.exe" -m pip install pygame
    if errorlevel 1 (
        echo ❌ Failed to install pygame.
        echo.
        echo The pygame installation failed. This might be due to:
        echo 1. Network connectivity issues
        echo 2. Insufficient disk space
        echo 3. Antivirus interference
        echo 4. Missing system dependencies
        echo.
        echo Try running this command manually:
        echo python\python.exe -m pip install pygame
        echo.
        echo If that works, the issue is with the script execution context.
        echo.
        pause
        exit /b 1
    ) else (
        echo ✅ Pygame installed successfully
    )
) else (
    echo ✅ Pygame is already installed
)

REM Verify pygame installation
echo 🔍 Verifying pygame installation...
call "%PYTHON_DIR%\python.exe" -c "import pygame; print('Pygame version:', pygame.version.ver)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Pygame import test failed!
    echo.
    echo This indicates pygame was not installed correctly.
    echo Please check the error messages above and try again.
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Pygame verification successful
)

REM Additional verification - test that pygame can create a display (basic functionality)
echo Testing pygame basic functionality...
call "%PYTHON_DIR%\python.exe" -c "import pygame; pygame.init(); print('Pygame initialized successfully'); pygame.quit()" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Warning: Basic pygame functionality test failed.
    echo The game may not display properly, but continuing...
) else (
    echo ✅ Pygame functionality test passed
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
