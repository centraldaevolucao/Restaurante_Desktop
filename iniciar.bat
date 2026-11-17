@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul && (py -3 restaurante_desktop.py %*) || (python restaurante_desktop.py %*)
if errorlevel 1 pause
