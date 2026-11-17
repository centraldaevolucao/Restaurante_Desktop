#!/usr/bin/env bash
# Restaurante Desktop (Linux) — precisa de Python 3.8+ (já vem na maioria das distribuições).
cd "$(dirname "$0")"
exec python3 restaurante_desktop.py "$@"
