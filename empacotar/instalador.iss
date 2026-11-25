; Inno Setup — instalador do Restaurante Desktop (Windows). Compile com:  iscc empacotar\instalador.iss
[Setup]
AppName=Restaurante
AppVersion=1.5.1
AppPublisher=Central da Evolução
DefaultDirName={autopf}\Restaurante
DefaultGroupName=Restaurante
OutputBaseFilename=Restaurante-desktop_v1.5.1-setup
OutputDir=..\saida
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "..\dist\Restaurante\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Restaurante"; Filename: "{app}\Restaurante.exe"
Name: "{autodesktop}\Restaurante"; Filename: "{app}\Restaurante.exe"

[Run]
; libera a porta 3000 na rede local para celulares e garçons acessarem este PC
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""Restaurante"" dir=in action=allow protocol=TCP localport=3000-3029 profile=private"; Flags: runhidden
Filename: "{app}\Restaurante.exe"; Description: "Abrir o Restaurante"; Flags: postinstall nowait skipifsilent

[UninstallRun]
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""Restaurante"""; Flags: runhidden
