@echo off 
 
echo 🗑️  Uninstalling Anime Monster Fighter... 
echo. 
 
REM Remove desktop shortcut 
if exist "%USERPROFILE%\Desktop\Anime Monster Fighter.lnk" del "%USERPROFILE%\Desktop\Anime Monster Fighter.lnk" 
 
REM Remove Start Menu entry 
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter" rmdir /s /q "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Anime Monster Fighter" 
 
REM Remove uninstaller itself 
del "%~f0" 
 
echo ✅ Uninstallation complete 
echo. 
pause 
