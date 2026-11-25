@echo off
title Build Discord Token Login GUI
echo.
echo  ================================
echo    Build Discord Token Login GUI
echo    Interface violet - GenZ 2026
echo  ================================
echo.
pip install pyinstaller PyQt5 undetected-chromedriver selenium --quiet
echo [*] Compilation...
pyinstaller --onefile --windowed ^
  --name "DiscordTokenLogin" ^
  --hidden-import=PyQt5 ^
  --hidden-import=PyQt5.QtWidgets ^
  --hidden-import=PyQt5.QtCore ^
  --hidden-import=PyQt5.QtGui ^
  --hidden-import=undetected_chromedriver ^
  --hidden-import=selenium ^
  discord_token_gui.py
copy "dist\DiscordTokenLogin.exe" "DiscordTokenLogin.exe" >nul
echo [+] Done — DiscordTokenLogin.exe prêt dans ce dossier.
pause
