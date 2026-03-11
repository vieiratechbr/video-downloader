import customtkinter as ctk
import threading
import requests
from PIL import Image
from io import BytesIO

from downloader import baixar_video, obter_info_video


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YouTube Downloader")

# tamanho inicial menor
app.geometry("520x500")


titulo = ctk.CTkLabel(app, text="YouTube Downloader", font=("Arial", 26))
titulo.pack(pady=20)


url_entry = ctk.CTkEntry(app, width=420, placeholder_text="Cole a URL do vídeo")
url_entry.pack(pady=10)


thumbnail_label = ctk.CTkLabel(app, text="")
thumbnail_label.pack(pady=10)


titulo_video = ctk.CTkLabel(app, text="")
titulo_video.pack()

canal_video = ctk.CTkLabel(app, text="")
canal_video.pack()

duracao_video = ctk.CTkLabel(app, text="")
duracao_video.pack(pady=5)


tipo_label = ctk.CTkLabel(app, text="Tipo de download")
tipo_label.pack(pady=10)


tipo_var = ctk.StringVar(value="")


opcoes_frame = ctk.CTkFrame(app)


qualidade_video_label = ctk.CTkLabel(opcoes_frame, text="Qualidade do vídeo")
qualidade_video_menu = ctk.CTkOptionMenu(opcoes_frame, values=["Aguardando vídeo..."])
qualidade_video_menu.set("Aguardando vídeo...")


qualidade_audio_label = ctk.CTkLabel(opcoes_frame, text="Qualidade do áudio")
qualidade_audio_menu = ctk.CTkOptionMenu(opcoes_frame, values=["320", "192", "128"])
qualidade_audio_menu.set("320")


def atualizar_opcoes():

    for widget in opcoes_frame.winfo_children():
        widget.destroy()

    opcoes_frame.pack(pady=10)

    if tipo_var.get() == "video":

        qualidade_video_label.pack(pady=5)
        qualidade_video_menu.pack()

    elif tipo_var.get() == "audio":

        qualidade_audio_label.pack(pady=5)
        qualidade_audio_menu.pack()


video_radio = ctk.CTkRadioButton(
    app,
    text="Vídeo",
    variable=tipo_var,
    value="video",
    command=atualizar_opcoes
)
video_radio.pack()


audio_radio = ctk.CTkRadioButton(
    app,
    text="Áudio (MP3)",
    variable=tipo_var,
    value="audio",
    command=atualizar_opcoes
)
audio_radio.pack(pady=5)


progress_bar = ctk.CTkProgressBar(app, width=420)
progress_bar.pack(pady=20)
progress_bar.set(0)


def atualizar_progresso(valor):

    def update():
        progress_bar.set(valor)

    app.after(0, update)


def formatar_duracao(segundos):

    minutos = segundos // 60
    segundos = segundos % 60

    return f"{minutos}:{segundos:02d}"


def carregar_video(event=None):

    url = url_entry.get()

    if not url:
        return

    def thread():

        info = obter_info_video(url)

        resolucoes = info["resolucoes"]
        resolucoes_formatadas = [f"{r}p" for r in resolucoes]

        thumb_url = info["thumbnail"]

        response = requests.get(thumb_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((320, 180))

        thumb = ctk.CTkImage(light_image=img, dark_image=img, size=(320,180))

        def update():

            qualidade_video_menu.configure(values=resolucoes_formatadas)
            qualidade_video_menu.set(resolucoes_formatadas[-1])

            titulo_video.configure(text=info["titulo"])
            canal_video.configure(text=f"Canal: {info['canal']}")
            duracao_video.configure(text=f"Duração: {formatar_duracao(info['duracao'])}")

            thumbnail_label.configure(image=thumb)
            thumbnail_label.image = thumb

            # 🔹 aumenta automaticamente a janela
            app.geometry("520x720")

        app.after(0, update)

    threading.Thread(target=thread).start()


url_entry.bind("<FocusOut>", carregar_video)
url_entry.bind("<Return>", carregar_video)


def iniciar_download():

    url = url_entry.get()
    tipo = tipo_var.get()

    if tipo == "video":
        qualidade = qualidade_video_menu.get().replace("p","")

    elif tipo == "audio":
        qualidade = qualidade_audio_menu.get()

    else:
        return

    progress_bar.set(0)

    def thread():
        baixar_video(url, tipo, qualidade, atualizar_progresso)

    threading.Thread(target=thread).start()


botao = ctk.CTkButton(app, text="Baixar", command=iniciar_download)
botao.pack(pady=20)


app.mainloop()