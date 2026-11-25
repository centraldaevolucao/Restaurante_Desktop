> **Versão atual do sistema: Restaurante-desktop 1.5.0 (núcleo 2.32.8)** — este arquivo é renomeado e atualizado a cada versão (seções numeradas abaixo, da mais antiga à mais nova).

# Restaurante Desktop — Windows e Linux

O mesmo sistema do app Android (Restaurante/Comandas) rodando no computador. Usa o **mesmo servidor, a mesma interface, o mesmo banco SQLite e o mesmo formato de backup**: um backup feito no celular restaura no PC e vice-versa.

## Como usar (sem instalar nada além do Python)
- **Windows:** dê dois cliques em `iniciar.bat` (precisa de Python 3.8+ instalado, marcando "Add to PATH").
- **Linux:** `./iniciar.sh` (Python 3 já vem na maioria das distribuições).
- O sistema abre numa janela própria (Edge/Chrome/Chromium) ou, se não houver, no navegador padrão.
- Os celulares e garçons da mesma rede acessam o PC pelo endereço mostrado na tela preta (`http://IP-do-PC:3000`), como acessam o aparelho servidor hoje. **Deixe a janela preta aberta** enquanto o sistema estiver em uso.
- Opções: `--sem-janela` (só o servidor), `--sem-tunel` (não gerar o link externo; por padrão ele é criado sozinho), `--pasta X` (guardar os dados em outra pasta).

## Onde ficam os dados
- Windows: `%APPDATA%\Restaurante` · Linux: `~/.local/share/restaurante`
- Banco: `data/database.sqlite`. Para copiar para outro aparelho, use o Backup do próprio sistema (Configurações → Backup).

## Licença (mesma regra do celular)
- A licença fica **presa a este computador**. O ID aparece em Assinatura e no terminal (formato `XXXX-XXXX`); o cliente o envia no pedido e você emite a licença no app Licenças, do mesmo jeito do celular.
- Mesmas edições e planos (Essencial, Gestão, Completo), plano grátis com 30 comandas por dia, teste de 30 dias uma vez por equipamento (a licença de teste emitida por você prevalece) e garantia de 35 dias.
- Trocar de PC ou reinstalar o sistema muda o ID: use a transferência de licença do app Licenças.

## Gerar os programas (.exe e Linux)
1. Sincronize o núcleo com o Android: `python empacotar/sincronizar_nucleo.py <pasta do comandas-apk>`.
2. **Windows:** `empacotar\build-windows.bat` gera `dist\Restaurante\Restaurante.exe`; com o Inno Setup, `iscc empacotar\instalador.iss` gera o instalador (libera a porta 3000–3029 no firewall para a rede privada).
3. **Linux:** `bash empacotar/build-linux.sh` gera `Restaurante-desktop_v1.0.0-linux-x64.tar.gz`.
4. Ou envie a tag `vX.Y.Z` ao GitHub: o fluxo `.github/workflows/build.yml` compila Windows e Linux sozinho (também roda a cada envio para a main e manualmente em Actions → build → Run workflow) e, na tag, publica a release com o instalador e o pacote Linux.
Nada é assinado digitalmente: o Windows pode mostrar o aviso "editor desconhecido" até haver certificado.

## Limites desta versão
- Não testado em Windows nem com impressora real; testado aqui em Linux (servidor, licença, dados, ID do equipamento e envio ESC/POS para uma impressora de rede simulada).
- Impressão: padrão pelo diálogo do sistema; térmica direta (rede, USB, serial, impressora do sistema) em Configurações → Impressoras. Bluetooth fica só no Android.
- Compartilhar/WhatsApp: abre o WhatsApp Web / baixa o arquivo, sem o menu "compartilhar" do Android.
- Sem ícone na bandeja nem atualização automática (planejados).

## Registro de alterações
### 1. v1.0.0 — Primeira versão desktop
- Launcher `restaurante_desktop.py` (Windows e Linux) que sobe o servidor do Android (núcleo 2.29.0) numa porta livre e abre a janela do sistema.
- Pasta de dados do sistema, ID do equipamento por computador (licença presa a ele), link externo opcional (`--tunel`).
- Scripts de empacotamento: PyInstaller (Windows e Linux), instalador Inno Setup com regra de firewall e fluxo do GitHub Actions.
- Sincronizador do núcleo para manter Android e Desktop no mesmo código.

### 2. v1.1.0 — Impressora térmica direta
- Impressoras de **rede (IP:9100)**, **USB**, **serial** e **instaladas no sistema** (Windows: fila RAW; Linux: CUPS `lp -o raw`) com a mesma tela e o mesmo layout (ESC/POS, acentos, QR, logo) usados na Bluetooth do Android.
- Em Impressoras → "Adicionar impressora de rede (IP)", informe IP e porta; escolha e toque em "Imprimir teste".
- **Linux/USB:** o usuário precisa de permissão no dispositivo (`/dev/usb/lp0`, normalmente grupo `lp`); ou instale a impressora no CUPS e use a opção "(CUPS)".
- Núcleo 2.30.0.

### 3. v1.1.1 — Cardápio QR para todos
- Núcleo 2.30.1: o cardápio digital por QR é bônus de todos, inclusive do plano grátis.

### 4. v1.1.2 — Fluxo do GitHub Actions
- O build agora roda ao enviar para a main, ao criar tag e **manualmente** (Actions → build → Run workflow); na tag, publica a Release com o instalador Windows e o pacote Linux.

### 5. v1.1.3 — Correção do build do Windows
- O fluxo agora chama `python -m PyInstaller` (o `py -3` podia usar outro Python sem o PyInstaller), confere se o `Restaurante.exe` foi gerado e localiza o Inno Setup automaticamente.
- O PyInstaller passa a analisar o núcleo (`server`, `licenca`, `backup_comandas`, `impressao`), para o programa empacotado não faltar módulos.
- `instalador.iss` salvo em UTF-8 com BOM (acentos).

### 6. v1.1.4 — Compartilhar backup
- Núcleo 2.30.2: o botão de compartilhar do backup usa o compartilhamento do sistema quando existe; senão baixa o arquivo e avisa a pasta Downloads.

### 7. v1.2.0 — Link externo automático
- Ao abrir, o programa **gera o link externo sozinho**: baixa o cloudflared na primeira vez (precisa de internet nesse momento) e cria o endereço `https://….trycloudflare.com`, que aparece em QR Codes e é usado nos QR Codes do cardápio. Nada para instalar.
- Opção `--sem-tunel` desliga o link automático. O link muda a cada abertura (é temporário).
- Ao baixar, a conexão é HTTPS direto do GitHub oficial da Cloudflare; o antivírus do Windows pode pedir confirmação na primeira execução do cloudflared.
- Núcleo 2.31.0.

### 8. v1.5.0 — Núcleo 2.32.8 (impressão A4, recibo em formato de nota, revisão LGPD/CDC)
- **Comanda e recibo:** campo "Imprimir em" — **Cupom** (padrão) ou **A4**; cadastro de impressoras A4 em Impressoras. No Windows/Linux a folha A4 sai pela janela de impressão do sistema, onde você escolhe a impressora.
- **Recibo A4 em formato de nota** (sem valor fiscal), com **QR Pix** enquanto aguarda pagamento e **várias páginas** quando necessário.
- **Termos, Privacidade, Reembolso e Créditos**, aceite registrado, "Privacidade e meus dados", senhas com hash e retenção automática. Detalhes em `CONFORMIDADE-LGPD-CDC.md` do app Android (mesmo núcleo).
- Os dados do aplicativo ficam na pasta do usuário (`%APPDATA%\Restaurante` / `~/.local/share/restaurante`); "Apagar dados pessoais" age sobre ela.

- Núcleo 2.32.8 inclui: comandas só são unidas pelo botão **Unir comandas** (seleção por comanda nas Pendências; recibo de uma comanda sai só dela) e WhatsApp do fornecedor com o telefone do cadastro.
- Núcleo 2.32.8: 'fiado' → 'Pendência'; WhatsApp envia a imagem do card direto ao contato (comanda, recibo e pendências).
- Núcleo 2.32.8: modelo A4 configurável (Configurações › Layout de impressão) com pré-visualização.
- Núcleo 2.32.8: Deixar Pendente pergunta se quer alterar o cliente já definido na comanda.
- Núcleo 2.32.8: recibo simples, cadastro Empresa, assinaturas do A4 e correção do corte ao compartilhar.
- Núcleo 2.32.8: recibo simples liberado ao finalizar a venda; A4 sem impressora cadastrada não bloqueia a visualização.
- Núcleo 2.32.8: recibo simples com CPF/CNPJ preenchidos e cidade/UF pelo GPS.
- Núcleo 2.32.8: recibo simples busca CPF/CNPJ só nos cadastros (sem campo de preenchimento na tela).

## Versão 1.5.0
- Núcleo 2.32.9: chat do suporte com novas seções (layouts de impressão, recibo A4/simples, Empresa, Pendências, privacidade).

## Versão 1.5.0
- Núcleo 2.32.10: interruptores para habilitar a impressão A4, Nota (NF) e Recibo simples.

## Versão 1.5.0
- Núcleo 2.32.11: removidos todos os trechos sobre IA (Créditos, Termos e Privacidade).

## Versão 1.5.0
- Núcleo 2.33.0: assinatura recorrente no cartão (Mercado Pago) com cancelamento no app; recurso liga quando o endereço do Servidor Assinatura é configurado (`COMANDAS_ASSINATURAS_URL` ou `data/assinaturas_url.txt`).

## Versão 1.5.0
- Núcleo 2.33.1: assinatura no cartão envia o nome do estabelecimento ao Servidor Assinatura.

## Versão 1.5.0
- Núcleo 2.34.0: plano Vitalício (licença sem vencimento).
