import yt_dlp


def baixar_video(url, tipo="video", qualidade="1080"):

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
            "noplaylist": True
        }

    else:

        if qualidade == "1080":
            formato = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif qualidade == "720":
            formato = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif qualidade == "480":
            formato = "bestvideo[height<=480]+bestaudio/best[height<=480]"
        else:
            formato = "bestvideo+bestaudio/best"

        opcoes = {
            "format": formato,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "ffmpeg_location": "./ffmpeg/bin",
            "merge_output_format": "mkv",
            "noplaylist": True
        }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])