import yt_dlp


def obter_info_video(url):

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(url, download=False)

        formatos = info.get("formats", [])

        resolucoes = set()

        for f in formatos:

            if f.get("vcodec") != "none":

                altura = f.get("height")

                if altura:
                    resolucoes.add(str(altura))

        resolucoes = sorted(resolucoes, key=lambda x: int(x))

        return {
            "titulo": info.get("title"),
            "canal": info.get("uploader"),
            "duracao": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "resolucoes": resolucoes
        }


def baixar_video(url, tipo="video", qualidade="1080", progress_callback=None):

    def hook(d):

        if d["status"] == "downloading":

            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            if total:

                percent = downloaded / total

                if progress_callback:
                    progress_callback(percent)

        elif d["status"] == "finished":

            if progress_callback:
                progress_callback(1)

    if tipo == "audio":

        opcoes = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "ffmpeg_location": "./ffmpeg/bin",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": qualidade,
            }],
            "progress_hooks": [hook],
            "noplaylist": True
        }

    else:

        formato = f"bestvideo[height<={qualidade}]+bestaudio/best[height<={qualidade}]"

        opcoes = {
            "format": formato,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "ffmpeg_location": "./ffmpeg/bin",
            "merge_output_format": "mkv",
            "progress_hooks": [hook],
            "noplaylist": True
        }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])