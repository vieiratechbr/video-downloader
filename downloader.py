import yt_dlp

url = input("Cole a URL do vídeo: ")

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

    # caminho do ffmpeg dentro do projeto
    "ffmpeg_location": "./ffmpeg/bin"
}

with yt_dlp.YoutubeDL(opcoes) as ydl:
    info = ydl.extract_info(url, download=False)

    print("\nTítulo:", info["title"])
    print("Iniciando download...\n")

    ydl.download([url])