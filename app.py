import customtkinter as ctk
import threading
from downloader import baixar_video


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("500x420")


titulo = ctk.CTkLabel(app, text="YouTube Downloader", font=("Arial", 24))
titulo.pack(pady=20)


url_entry = ctk.CTkEntry(app, width=400, placeholder_text="Cole a URL do vídeo")
url_entry.pack(pady=10)


tipo_label = ctk.CTkLabel(app, text="Tipo de download")
tipo_label.pack()


tipo_var = ctk.StringVar(value="")


# FRAME DAS OPÇÕES DINÂMICAS
opcoes_frame = ctk.CTkFrame(app)
opcoes_frame.pack(pady=10)


# QUALIDADE VIDEO
qualidade_video_label = ctk.CTkLabel(opcoes_frame, text="Qualidade do vídeo")
qualidade_video_menu = ctk.CTkOptionMenu(opcoes_frame, values=["1080", "720", "480"])
qualidade_video_menu.set("1080")


# QUALIDADE AUDIO
qualidade_audio_label = ctk.CTkLabel(opcoes_frame, text="Qualidade do áudio (kbps)")
qualidade_audio_menu = ctk.CTkOptionMenu(opcoes_frame, values=["320", "192", "128"])
qualidade_audio_menu.set("320")


def atualizar_opcoes():

    for widget in opcoes_frame.winfo_children():
        widget.pack_forget()

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


status_label = ctk.CTkLabel(app, text="")
status_label.pack(pady=15)


def iniciar_download():

    url = url_entry.get()
    tipo = tipo_var.get()

    if tipo == "video":
        qualidade = qualidade_video_menu.get()

    elif tipo == "audio":
        qualidade = qualidade_audio_menu.get()

    else:
        status_label.configure(text="Escolha vídeo ou áudio")
        return

    if not url:
        status_label.configure(text="Cole uma URL primeiro")
        return

    status_label.configure(text="Baixando...")

    def download_thread():
        try:
            baixar_video(url, tipo, qualidade)
            status_label.configure(text="Download concluído!")
        except:
            status_label.configure(text="Erro no download")

    threading.Thread(target=download_thread).start()


# BOTÃO SEMPRE NO FINAL
botao = ctk.CTkButton(app, text="Baixar", command=iniciar_download)
botao.pack(pady=20)


app.mainloop()