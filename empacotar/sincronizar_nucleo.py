#!/usr/bin/env python3
"""Copia o núcleo do app Android (server.py, licenca.py, backup_comandas.py e a interface public/)
para esta pasta, para que Android e Desktop usem SEMPRE o mesmo código.
Uso: python empacotar/sincronizar_nucleo.py <pasta do comandas-apk> [<pasta public>]"""
import shutil, sys
from pathlib import Path
raiz = Path(__file__).resolve().parent.parent
apk = Path(sys.argv[1]).resolve()
py = apk / "app/src/main/python"
destino = raiz / "nucleo"
for f in ("server.py", "licenca.py", "backup_comandas.py"):
    shutil.copy2(py / f, destino / f)
if (destino / "public").exists():
    shutil.rmtree(destino / "public")
if len(sys.argv) > 2:
    shutil.copytree(sys.argv[2], destino / "public")
else:
    import zipfile
    with zipfile.ZipFile(apk / "app/src/main/assets/public.zip") as z:
        z.extractall(destino / "public")
print("Núcleo sincronizado de", apk)
