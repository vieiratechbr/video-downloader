import yt_dlp

url = input("Cole a URL do vídeo: ")

print("\nO que você deseja baixar?")
print("1 - Vídeo")
print("2 - Áudio (MP3)")

tipo = input("Escolha uma opção: ")

# ==============================
# DOWNLOAD DE VÍDEO
# ==============================

if tipo == "1":

    print("\nEscolha a qualidade:")
    print("1 - 1080p")
    print("2 - 720p")
    print("3 - 480p")

    escolha = input("Digite o número da qualidade: ")

    qualidades = {
        "1": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "2": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "3": "bestvideo[height<=480]+bestaudio/best[height<=480]"
    }

    formato = qualidades.get(escolha)

    if not formato:
        print("Qualidade inválida!")
        exit()

    opcoes = {
        "format": formato,
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "ffmpeg_location": "./ffmpeg/bin"
    }

# ==============================
# DOWNLOAD DE ÁUDIO
# ==============================

elif tipo == "2":

    opcoes = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "ffmpeg_location": "./ffmpeg/bin",

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

else:
    print("Opção inválida!")
    exit()

# ==============================
# EXECUTAR DOWNLOAD
# ==============================

with yt_dlp.YoutubeDL(opcoes) as ydl:
    info = ydl.extract_info(url, download=False)

    print("\nTítulo:", info["title"])
    print("Iniciando download...\n")

    ydl.download([url])