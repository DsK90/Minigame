@echo off 
setlocal enabledelayedexpansion 
 
echo 🗑️  Uninstalling Anime Monster Fighter... 
echo ======================================== 
echo. 
echo This will remove the portable installation. 
echo. 
 
REM Remove desktop shortcut 
if exist "%USERPROFILE%\Desktop\Anime Monster Fighter.lnk" del "%USERPROFILE%\Desktop\Anime Monster Fighter.lnk" 
 
REM Remove Start Menu entry 
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter" rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter" 
 
REM Remove portable Python and packages 
if exist "python" rmdir /s /q "python" 
 
REM Remove game files (optional - comment out if you want to keep them) 
REM if exist "game.py" del "game.py" 
REM if exist "player.py" del "player.py" 
REM if exist "monster.py" del "monster.py" 
REM if exist "clay_pot.py" del "clay_pot.py" 
 
echo. 
echo ✅ Portable uninstallation complete 
echo. 
echo Note: Game source files were preserved. 
echo Delete them manually if you want to remove everything. 
 
pause 
