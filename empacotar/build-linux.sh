#!/usr/bin/env bash
# Gera dist/Restaurante/Restaurante (Linux) e o pacote .tar.gz. Requer: pip install pyinstaller
set -e
cd "$(dirname "$0")/.."
python3 -m PyInstaller --noconfirm --clean --name Restaurante \
  --add-data "nucleo:nucleo" --hidden-import sqlite3 restaurante_desktop.py
tar -czf Restaurante-desktop_v1.1.1-linux-x64.tar.gz -C dist Restaurante
echo "Pronto: Restaurante-desktop_v1.1.1-linux-x64.tar.gz"
