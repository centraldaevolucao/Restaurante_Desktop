#!/usr/bin/env python3
"""Restaurante Desktop 1.3.10 — Windows e Linux.

Sobe o MESMO servidor do app Android (nucleo/server.py) e abre o sistema numa janela do navegador.
Dados, backup e licença seguem as mesmas regras do celular (licença presa a este computador).

Uso:
    python restaurante_desktop.py            abre o sistema (porta 3000; se ocupada, a próxima livre)
    python restaurante_desktop.py --sem-janela   só o servidor (modo servidor/headless)
    python restaurante_desktop.py --sem-tunel   não gera o link externo (por padrão ele é criado sozinho)
    python restaurante_desktop.py --pasta X  guarda os dados em X (padrão: pasta do sistema)
"""
import os, sys, re, json, time, uuid, shutil, socket, subprocess, threading, webbrowser, hashlib
from pathlib import Path
import urllib.request

VERSAO_DESKTOP = "1.3.10"
NOME = "Restaurante"


def pasta_app():
    """Onde estão os arquivos do programa (também dentro do pacote PyInstaller)."""
    return Path(getattr(sys, "_MEIPASS", None) or Path(__file__).resolve().parent)


def pasta_dados(forcada=None):
    if forcada:
        return Path(forcada).expanduser().resolve()
    if os.name == "nt":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(base) / NOME
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / NOME.lower()


def id_equipamento(raiz):
    """ID do COMPUTADOR (a licença fica presa a ele, como o Android ID no celular).
    Windows: MachineGuid; Linux: machine-id; senão um UUID gravado na pasta de dados."""
    bruto = ""
    try:
        if os.name == "nt":
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography", 0,
                                winreg.KEY_READ | getattr(winreg, "KEY_WOW64_64KEY", 0)) as k:
                bruto = str(winreg.QueryValueEx(k, "MachineGuid")[0]).strip()
        else:
            for c in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
                try:
                    bruto = Path(c).read_text().strip()
                except OSError:
                    continue
                if bruto:
                    break
    except Exception:
        bruto = ""
    arq = raiz / "equipamento.id"
    if not bruto:
        try:
            bruto = arq.read_text().strip()
        except OSError:
            bruto = ""
        if not bruto:
            bruto = uuid.uuid4().hex
    # nunca expõe o identificador cru do sistema: usa um resumo dele, com prefixo da plataforma
    resumo = hashlib.sha256(("restaurante-desktop|" + bruto).encode()).hexdigest()[:32]
    ident = ("WIN-" if os.name == "nt" else "LNX-") + resumo
    try:
        raiz.mkdir(parents=True, exist_ok=True)
        if not arq.exists():
            arq.write_text(ident)
    except OSError:
        pass
    return ident


def versao_nucleo(nucleo):
    try:
        m = re.search(r'VERSAO_SERVIDOR\s*=\s*"([^"]+)"', (nucleo / "server.py").read_text(encoding="utf-8"))
        return m.group(1) if m else "?"
    except OSError:
        return "?"


def preparar_pasta(raiz, nucleo):
    """server.py espera ROOT/public e ROOT/data. A cópia da interface é refeita quando o programa é atualizado."""
    raiz.mkdir(parents=True, exist_ok=True)
    marca = raiz / ".versao-interface"
    atual = VERSAO_DESKTOP + "+" + versao_nucleo(nucleo)
    destino = raiz / "public"
    try:
        igual = marca.read_text().strip() == atual
    except OSError:
        igual = False
    if not igual or not destino.is_dir():
        if destino.exists():
            shutil.rmtree(destino)
        shutil.copytree(nucleo / "public", destino)
        marca.write_text(atual)


def porta_livre(inicial):
    for p in range(inicial, inicial + 30):
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    raise SystemExit("Nenhuma porta livre entre %d e %d." % (inicial, inicial + 29))


def ja_rodando(porta):
    try:
        with urllib.request.urlopen("http://127.0.0.1:%d/api/info-servidor" % porta, timeout=1.5) as r:
            return r.status == 200
    except Exception:
        return False


def abrir_janela(url):
    """Abre como aplicativo (sem barra de endereço) no Edge/Chrome/Chromium; senão, no navegador padrão."""
    candidatos = []
    if os.name == "nt":
        for var in ("PROGRAMFILES(X86)", "PROGRAMFILES", "LOCALAPPDATA"):
            b = os.environ.get(var)
            if b:
                candidatos += [Path(b) / "Microsoft/Edge/Application/msedge.exe", Path(b) / "Google/Chrome/Application/chrome.exe"]
    else:
        for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser"):
            c = shutil.which(n)
            if c:
                candidatos.append(Path(c))
    for exe in candidatos:
        if exe.is_file():
            try:
                subprocess.Popen([str(exe), "--app=" + url, "--window-size=1200,800"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except OSError:
                pass
    webbrowser.open(url)


def main(argv):
    if sys.stdout is None or sys.stderr is None:      # sem console: registra num arquivo em vez de falhar
        log = open(pasta_dados() / "restaurante.log", "a", encoding="utf-8", buffering=1) if pasta_dados().is_dir() else open(os.devnull, "w")
        sys.stdout = sys.stdout or log
        sys.stderr = sys.stderr or log
    sem_janela = "--sem-janela" in argv
    com_tunel = "--sem-tunel" not in argv and os.environ.get("RESTAURANTE_SEM_TUNEL") != "1"
    forcada = argv[argv.index("--pasta") + 1] if "--pasta" in argv and argv.index("--pasta") + 1 < len(argv) else None
    nucleo = pasta_app() / "nucleo"
    if not (nucleo / "server.py").is_file():          # rodando direto da pasta do projeto
        nucleo = Path(__file__).resolve().parent / "nucleo"
    raiz = pasta_dados(forcada)
    preparar_pasta(raiz, nucleo)

    porta_pref = int(os.environ.get("PORT", "3000"))
    if ja_rodando(porta_pref):
        print("O Restaurante já está aberto neste computador. Abrindo a janela…")
        if not sem_janela:
            abrir_janela("http://localhost:%d/" % porta_pref)
        return 0
    porta = porta_livre(porta_pref)

    sys.path.insert(0, str(nucleo))
    os.environ["COMANDAS_ROOT"] = str(raiz)
    os.environ["COMANDAS_EQUIP"] = os.environ.get("COMANDAS_EQUIP") or id_equipamento(raiz)
    os.environ.setdefault("HOST", "0.0.0.0")     # celulares e garçons da mesma rede acessam este PC
    os.environ["PORT"] = str(porta)
    import server                                # lê as variáveis acima ao ser importado

    server.init_db()
    srv = server.ThreadingHTTPServer((server.HOST, server.PORT), server.Handler)
    threading.Thread(target=srv.serve_forever, name="restaurante-servidor", daemon=True).start()

    print("Restaurante Desktop %s (núcleo %s)" % (VERSAO_DESKTOP, server.VERSAO_SERVIDOR))
    print("  Dados:        %s" % raiz)
    print("  Neste PC:     http://localhost:%d" % porta)
    try:
        print("  Outros aparelhos da rede: http://%s:%d" % (server.local_ip(), porta))
    except Exception:
        pass
    print("  ID do equipamento (licença): %s" % server.LIC.instalacao_id)
    if com_tunel:                                    # link externo automático (baixa o cloudflared sozinho na 1ª vez)
        try:
            import tunel
            tunel.init(raiz, porta)
            tunel.iniciar()
            print("  Link externo: sendo criado (aparece em QR Codes quando ficar pronto)…")
        except Exception as e:
            print("  (link externo indisponível: %s)" % e)
    if not sem_janela:
        abrir_janela("http://localhost:%d/" % porta)
    print("Feche esta janela ou pressione Ctrl+C para encerrar o servidor.")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        if com_tunel:
            try:
                tunel.parar()
            except Exception:
                pass
        srv.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
