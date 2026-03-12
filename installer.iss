; =========================================================
; YouTube Downloader Installer
; Autor: Nathan Moura Vieira
; Ferramenta: Inno Setup
; =========================================================

; =========================================================
; BLOCO [Setup]
; Configurações principais do instalador
; =========================================================
[Setup]
; ID único do aplicativo no Windows
AppId={{E2A3F7A1-3C7B-4F88-9B11-7D89F4B61A21}}

; Nome exibido do aplicativo
AppName=YouTube Downloader

; Versão do aplicativo
AppVersion=1.0.1

; Nome do autor/publicador
AppPublisher=Nathan Moura Vieira

; Links do projeto
AppPublisherURL=https://github.com/vieiratechbr
AppSupportURL=https://github.com/vieiratechbr
AppUpdatesURL=https://github.com/vieiratechbr/video-downloader

; Pasta padrão de instalação
DefaultDirName={autopf}\Vieira Tech\YouTube Downloader

; Nome da pasta no Menu Iniciar
DefaultGroupName=YouTube Downloader

; Oculta a etapa de escolher pasta do menu iniciar
DisableProgramGroupPage=yes

; Arquivo de licença mostrado durante a instalação
LicenseFile=LICENSE.txt

; Diretório onde o instalador final será gerado
OutputDir=installer_output

; Nome do arquivo final do instalador
OutputBaseFilename=YouTubeDownloaderSetup_v1.0.1

; Compactação do instalador
Compression=lzma
SolidCompression=yes

; Estilo visual moderno do instalador
WizardStyle=modern

; Ícone do instalador (opcional)
SetupIconFile=icon.ico

; Ícone mostrado no painel de aplicativos instalados
UninstallDisplayIcon={app}\YouTube Downloader.exe

; Arquitetura permitida
ArchitecturesInstallIn64BitMode=x64compatible

; Nome visível na lista de programas instalados
UninstallDisplayName=YouTube Downloader

; Diretório padrão temporário para o instalador
PrivilegesRequired=admin


; =========================================================
; BLOCO [Languages]
; Idioma do instalador
; =========================================================
[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"


; =========================================================
; BLOCO [Tasks]
; Opções adicionais mostradas para o usuário
; =========================================================
[Tasks]
; Checkbox para criar atalho na área de trabalho
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Opções adicionais:"; Flags: unchecked

; Checkbox opcional para abrir o GitHub depois (pode deixar ou remover)
Name: "opengithub"; Description: "Abrir página do projeto no GitHub após a instalação"; GroupDescription: "Opções adicionais:"; Flags: unchecked


; =========================================================
; BLOCO [Files]
; Arquivos que serão copiados para a pasta de instalação
; =========================================================
[Files]
; Copia tudo da pasta gerada pelo PyInstaller
Source: "dist\YouTube Downloader\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion


; =========================================================
; BLOCO [Icons]
; Atalhos criados pelo instalador
; =========================================================
[Icons]
; Atalho no Menu Iniciar
Name: "{group}\YouTube Downloader"; Filename: "{app}\YouTube Downloader.exe"; IconFilename: "{app}\YouTube Downloader.exe"

; Atalho para desinstalar
Name: "{group}\Desinstalar YouTube Downloader"; Filename: "{uninstallexe}"

; Atalho opcional na área de trabalho
Name: "{autodesktop}\YouTube Downloader"; Filename: "{app}\YouTube Downloader.exe"; Tasks: desktopicon; IconFilename: "{app}\YouTube Downloader.exe"


; =========================================================
; BLOCO [Run]
; Ações opcionais ao final da instalação
; =========================================================
[Run]
; Executa o aplicativo após instalar
Filename: "{app}\YouTube Downloader.exe"; Description: "Executar YouTube Downloader"; Flags: nowait postinstall skipifsilent

; Abre o GitHub após instalar, se o usuário marcar a opção
Filename: "https://github.com/vieiratechbr"; Description: "Abrir projeto no GitHub"; Flags: postinstall shellexec skipifsilent; Tasks: opengithub


; =========================================================
; BLOCO [Code]
; Personalizações visuais e pequenos ajustes
; =========================================================
[Code]
procedure InitializeWizard;
begin
 
  WizardForm.WelcomeLabel1.Caption := 'Bem-vindo ao instalador do YouTube Downloader';
  WizardForm.WelcomeLabel2.Caption := 'Este assistente irá instalar o aplicativo no seu computador.';
end;