import os
import sys
import shutil
from pathlib import Path

import yt_dlp


APP_NAME = "YouTube Downloader"


def _resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def _get_download_dir() -> str:
    pasta = os.path.join(Path.home(), "Downloads", APP_NAME)
    os.makedirs(pasta, exist_ok=True)
    return pasta


def pasta_downloads_atual() -> str:
    return _get_download_dir()


def _get_ffmpeg_location():
    candidatos = [
        _resource_path("ffmpeg/bin"),
        _resource_path("bin"),
        os.path.join(os.path.abspath("."), "ffmpeg", "bin"),
    ]

    for pasta in candidatos:
        ffmpeg_exe = os.path.join(pasta, "ffmpeg.exe")
        ffprobe_exe = os.path.join(pasta, "ffprobe.exe")
        if os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe):
            return pasta

    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        return os.path.dirname(ffmpeg_path)

    return None


def _get_js_runtimes():
    runtimes = []

    deno = shutil.which("deno")
    if deno:
        runtimes.append(f"deno:{deno}")

    node = shutil.which("node")
    if node:
        runtimes.append(f"node:{node}")

    if runtimes:
        return ",".join(runtimes)

    return None


def _detectar_cookies_from_browser():
    local = os.environ.get("LOCALAPPDATA", "")
    roaming = os.environ.get("APPDATA", "")

    navegadores = [
        ("chrome", os.path.join(local, "Google", "Chrome", "User Data")),
        ("edge", os.path.join(local, "Microsoft", "Edge", "User Data")),
        ("brave", os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data")),
        ("vivaldi", os.path.join(local, "Vivaldi", "User Data")),
        ("firefox", os.path.join(roaming, "Mozilla", "Firefox")),
        ("opera", os.path.join(roaming, "Opera Software")),
    ]

    for nome, caminho in navegadores:
        if caminho and os.path.exists(caminho):
            return (nome,)

    return None


def _sanitize_error_message(msg: str) -> str:
    msg = (msg or "").strip()

    if "Sign in to confirm you’re not a bot" in msg or "Sign in to confirm you're not a bot" in msg:
        return (
            "O YouTube bloqueou este download. "
            "Faça login no YouTube no navegador da máquina e tente novamente."
        )

    if "No supported JavaScript runtime could be found" in msg:
        return (
            "Runtime JavaScript não encontrado. "
            "Instale Deno ou Node.js."
        )

    if "ffmpeg" in msg.lower():
        return (
            "FFmpeg não encontrado. "
            "Inclua ffmpeg.exe e ffprobe.exe no instalador ou instale FFmpeg no Windows."
        )

    if "Invalid js_runtimes format" in msg:
        return (
            "Configuração de runtime JavaScript inválida. "
            "Feche o app, salve este arquivo atualizado e rode novamente."
        )

    return msg


def _base_ydl_opts(progress_callback=None) -> dict:
    def hook(d):
        status = d.get("status")

        if status == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            if total and progress_callback:
                percent = max(0, min(downloaded / total, 1))
                progress_callback(percent)

        elif status == "finished":
            if progress_callback:
                progress_callback(1)

    opts = {
        "noplaylist": True,
        "quiet": True,
        "restrictfilenames": False,
        "windowsfilenames": True,
        "nopart": False,
        "retries": 10,
        "fragment_retries": 10,
        "progress_hooks": [hook],
    }

    ffmpeg_location = _get_ffmpeg_location()
    if ffmpeg_location:
        opts["ffmpeg_location"] = ffmpeg_location

    return opts


def obter_info_video(url):
    ydl_opts = _base_ydl_opts()
    ydl_opts.update({
        "skip_download": True,
        "extract_flat": False,
    })

    try:
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

    except Exception as e:
        raise RuntimeError(_sanitize_error_message(str(e))) from e


def baixar_video(url, tipo="video", qualidade="1080", rapido=False, progress_callback=None):
    pasta_saida = _get_download_dir()
    outtmpl = os.path.join(pasta_saida, "%(title)s.%(ext)s")

    opcoes = _base_ydl_opts(progress_callback)
    opcoes["outtmpl"] = outtmpl

    try:
        if tipo == "audio":
            opcoes.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": str(qualidade),
                }],
            })
        else:
            if rapido:
                formato = f"best[height<={qualidade}]"
            else:
                formato = f"bestvideo[height<={qualidade}]+bestaudio/best"

            opcoes.update({
                "format": formato,
            })

            if not rapido:
                opcoes["merge_output_format"] = "mkv"

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        return pasta_saida

    except Exception as e:
        raise RuntimeError(_sanitize_error_message(str(e))) from e