import yt_dlp

url = input("Cole a URL do vídeo: ")

opcoes = {
    "outtmpl": "downloads/%(title)s.%(ext)s"
}

with yt_dlp.YoutubeDL(opcoes) as ydl:
    info = ydl.extract_info(url, download=False)
    print("Título:", info["title"])

    ydl.download([url])