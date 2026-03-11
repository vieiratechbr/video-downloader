# YouTube Downloader

Aplicativo desktop para baixar vídeos e áudios do YouTube com interface gráfica moderna, suporte a múltiplas qualidades, preview do vídeo, barra de progresso e alternância de idioma/tema.

## Preview

O aplicativo permite:

- colar o link do vídeo
- carregar automaticamente thumbnail, título, canal e duração
- escolher entre baixar vídeo ou áudio
- selecionar a qualidade disponível
- usar modo de download rápido
- acompanhar o progresso do download em tempo real
- alternar entre modo claro e escuro
- alternar idioma entre português e inglês

## Funcionalidades

### Download de vídeo
- Download em diferentes resoluções
- Detecção automática das qualidades disponíveis no vídeo
- Suporte a FFmpeg para combinação de áudio e vídeo
- Opção de download rápido

### Download de áudio
- Conversão para MP3
- Seleção de qualidade de áudio

### Interface gráfica
- Interface feita com CustomTkinter
- Thumbnail do vídeo
- Exibição de título, canal e duração
- Barra de progresso
- Modo claro/escuro
- Suporte a múltiplos idiomas

### Extras
- Popup ao fechar o aplicativo com link para o GitHub
- Tooltip explicando o modo de download rápido

## Tecnologias utilizadas

- Python
- CustomTkinter
- yt-dlp
- FFmpeg
- Requests
- Pillow

## Estrutura do projeto

```bash
Video Downloader/
├── app.py
├── downloader.py
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
├── downloads/
└── README.md
