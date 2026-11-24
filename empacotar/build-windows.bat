@echo off
rem Gera dist\Restaurante\Restaurante.exe (Windows). Requer Python 3.10+ e: pip install pyinstaller
cd /d "%~dp0.."
py -3 -m PyInstaller --noconfirm --clean --name Restaurante ^
  --add-data "nucleo;nucleo" --paths nucleo --hidden-import server --hidden-import licenca --hidden-import backup_comandas --hidden-import impressao --hidden-import tunel --hidden-import cartao --hidden-import sqlite3 restaurante_desktop.py
rem Instalador (opcional): instale o Inno Setup e rode:  iscc empacotar\instalador.iss
