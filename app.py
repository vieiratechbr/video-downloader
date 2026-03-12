import customtkinter as ctk
import threading
import requests
import webbrowser
from PIL import Image
from io import BytesIO

from downloader import baixar_video, obter_info_video

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

ACCENT = "#22b8cf"
ACCENT_HOVER = "#1ca3b8"
GITHUB_URL = "https://github.com/vieiratechbr"


TEXTS = {
    "pt": {
        "app_title": "⬇️ YouTube Downloader",
        "app_subtitle": "Baixe vídeos e áudio com interface moderna",
        "theme_light": "☀️ Claro",
        "theme_dark": "🌙 Escuro",
        "url_label": "🔗 URL do vídeo",
        "url_placeholder": "Cole a URL do vídeo aqui",
        "preview_title": "🎬 Preview do vídeo",
        "preview_wait_thumb": "Cole um link do YouTube para carregar a thumbnail",
        "video_title_placeholder": "Título do vídeo",
        "channel_placeholder": "📺 Canal: -",
        "duration_placeholder": "⏱ Duração: -",
        "status_waiting": "Aguardando link...",
        "download_type": "⚙️ Tipo de download",
        "video": "Vídeo",
        "audio": "Áudio (MP3)",
        "quality_title": "🎚️ Qualidade",
        "video_quality": "Qualidade do vídeo",
        "audio_quality": "Qualidade do áudio",
        "waiting_video": "Aguardando vídeo...",
        "no_options": "Sem opções",
        "fast_download": "Download rápido",
        "fast_tooltip": (
            "O download rápido tenta baixar um arquivo único para acelerar o processo.\n\n"
            "Nem sempre ele mantém áudio e vídeo juntos em todos os vídeos.\n"
            "Isso depende dos formatos disponíveis no vídeo escolhido."
        ),
        "progress_title": "📥 Progresso do download",
        "download_button": "⬇️ Baixar",
        "status_loading_video": "Carregando informações do vídeo...",
        "status_video_loaded": "Vídeo carregado com sucesso.",
        "status_invalid_video": "Não foi possível carregar este vídeo.",
        "status_check_link": "Verifique o link e tente novamente.",
        "thumb_unavailable": "Thumbnail indisponível",
        "thumb_load_error": "Não foi possível carregar a thumbnail",
        "title_unavailable": "Título indisponível",
        "status_paste_url": "Cole uma URL antes de baixar.",
        "status_choose_type": "Escolha vídeo ou áudio antes de baixar.",
        "status_starting_download": "Iniciando download...",
        "status_download_success": "Download concluído com sucesso.",
        "status_download_error": "Erro ao baixar o arquivo.",
        "popup_title": "⭐ Gostou do aplicativo?",
        "popup_text": "Se curtiu o app, me siga ou avalie no GitHub.\nIsso ajuda bastante o projeto a crescer.",
        "popup_checkbox": "Não mostrar novamente nesta sessão",
        "popup_open_github": "💙 Abrir GitHub",
        "popup_close_app": "Fechar aplicativo",
        "language_pt": "PT",
        "language_en": "EN",
        "channel_prefix": "📺 Canal: ",
        "duration_prefix": "⏱ Duração: "
    },
    "en": {
        "app_title": "⬇️ YouTube Downloader",
        "app_subtitle": "Download videos and audio with a modern interface",
        "theme_light": "☀️ Light",
        "theme_dark": "🌙 Dark",
        "url_label": "🔗 Video URL",
        "url_placeholder": "Paste the video URL here",
        "preview_title": "🎬 Video Preview",
        "preview_wait_thumb": "Paste a YouTube link to load the thumbnail",
        "video_title_placeholder": "Video title",
        "channel_placeholder": "📺 Channel: -",
        "duration_placeholder": "⏱ Duration: -",
        "status_waiting": "Waiting for link...",
        "download_type": "⚙️ Download type",
        "video": "Video",
        "audio": "Audio (MP3)",
        "quality_title": "🎚️ Quality",
        "video_quality": "Video quality",
        "audio_quality": "Audio quality",
        "waiting_video": "Waiting for video...",
        "no_options": "No options",
        "fast_download": "Fast download",
        "fast_tooltip": (
            "Fast download tries to fetch a single file to speed up the process.\n\n"
            "It may not always keep audio and video together for every video.\n"
            "This depends on the formats available for the selected video."
        ),
        "progress_title": "📥 Download progress",
        "download_button": "⬇️ Download",
        "status_loading_video": "Loading video information...",
        "status_video_loaded": "Video loaded successfully.",
        "status_invalid_video": "Could not load this video.",
        "status_check_link": "Check the link and try again.",
        "thumb_unavailable": "Thumbnail unavailable",
        "thumb_load_error": "Could not load thumbnail",
        "title_unavailable": "Title unavailable",
        "status_paste_url": "Paste a URL before downloading.",
        "status_choose_type": "Choose video or audio before downloading.",
        "status_starting_download": "Starting download...",
        "status_download_success": "Download completed successfully.",
        "status_download_error": "Error downloading the file.",
        "popup_title": "⭐ Enjoyed the app?",
        "popup_text": "If you liked the app, follow me or rate it on GitHub.\nThat really helps the project grow.",
        "popup_checkbox": "Do not show again in this session",
        "popup_open_github": "💙 Open GitHub",
        "popup_close_app": "Close application",
        "language_pt": "PT",
        "language_en": "EN",
        "channel_prefix": "📺 Channel: ",
        "duration_prefix": "⏱ Duration: "
    }
}


app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("700x820")
app.resizable(False, False)

idioma_atual = ctk.StringVar(master=app, value="pt")
url_var = ctk.StringVar(master=app)
tipo_var = ctk.StringVar(master=app, value="")
rapido_var = ctk.BooleanVar(master=app, value=False)
nao_mostrar_popup_saida = ctk.BooleanVar(master=app, value=False)


def t(key):
    return TEXTS[idioma_atual.get()][key]


class ToolTip:
    def __init__(self, widget, text_func):
        self.widget = widget
        self.text_func = text_func
        self.tooltip_window = None

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window is not None:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tooltip_window = ctk.CTkToplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.geometry(f"+{x}+{y}")

        label = ctk.CTkLabel(
            self.tooltip_window,
            text=self.text_func(),
            justify="left",
            wraplength=280,
            corner_radius=10,
            fg_color=("#dbeafe", "#1f2937"),
            text_color=("#0f172a", "#f8fafc"),
            padx=12,
            pady=8
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window is not None:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def alternar_tema():
    modo_atual = ctk.get_appearance_mode()

    if modo_atual == "Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

    atualizar_textos_interface()


def formatar_duracao(segundos):
    if segundos is None:
        return "0:00"

    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60

    if horas > 0:
        return f"{horas}:{minutos:02d}:{segundos:02d}"
    return f"{minutos}:{segundos:02d}"


ultimo_url_carregado = {"url": None}
carregamento_agendado = {"id": None}
popup_saida_aberto = {"valor": False}
ultimo_info_video = {
    "titulo": None,
    "canal": None,
    "duracao": None,
    "thumb_ok": False,
    "status_key": "status_waiting"
}


top_bar = ctk.CTkFrame(app, fg_color="transparent")
top_bar.pack(fill="x", padx=20, pady=(18, 10))

titulo_container = ctk.CTkFrame(top_bar, fg_color="transparent")
titulo_container.pack(side="left")

app_title = ctk.CTkLabel(
    titulo_container,
    text=t("app_title"),
    font=("Arial", 28, "bold"),
    text_color=("#0f172a", "#ecfeff")
)
app_title.pack(anchor="w")

app_subtitle = ctk.CTkLabel(
    titulo_container,
    text=t("app_subtitle"),
    font=("Arial", 13),
    text_color=("gray30", "gray75")
)
app_subtitle.pack(anchor="w", pady=(2, 0))

controls_container = ctk.CTkFrame(top_bar, fg_color="transparent")
controls_container.pack(side="right")

tema_btn = ctk.CTkButton(
    controls_container,
    text=t("theme_light"),
    width=120,
    height=38,
    corner_radius=14,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER,
    text_color="white",
    command=alternar_tema
)
tema_btn.pack(anchor="e")

language_menu = ctk.CTkOptionMenu(
    controls_container,
    values=[t("language_pt"), t("language_en")],
    width=70,
    height=26,
    corner_radius=10,
    fg_color=ACCENT,
    button_color=ACCENT_HOVER,
    button_hover_color="#168ea0",
    font=("Arial", 11)
)
language_menu.pack(anchor="e", pady=(6, 0))


main_card = ctk.CTkFrame(app, corner_radius=20)
main_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))


url_section = ctk.CTkFrame(main_card, fg_color="transparent")
url_section.pack(fill="x", padx=22, pady=(20, 12))

url_label = ctk.CTkLabel(
    url_section,
    text=t("url_label"),
    font=("Arial", 15, "bold")
)
url_label.pack(anchor="w", pady=(0, 8))

url_entry = ctk.CTkEntry(
    url_section,
    width=620,
    height=44,
    textvariable=url_var,
    placeholder_text=t("url_placeholder")
)
url_entry.pack(fill="x")


preview_card = ctk.CTkFrame(main_card, corner_radius=18)
preview_card.pack(fill="x", padx=22, pady=(0, 14))

preview_title = ctk.CTkLabel(
    preview_card,
    text=t("preview_title"),
    font=("Arial", 15, "bold")
)
preview_title.pack(anchor="w", padx=16, pady=(14, 10))

preview_content = ctk.CTkFrame(preview_card, fg_color="transparent")
preview_content.pack(fill="x", padx=16, pady=(0, 14))

thumbnail_label = ctk.CTkLabel(
    preview_content,
    text=t("preview_wait_thumb"),
    width=320,
    height=180,
    corner_radius=14,
    fg_color=("#dbeafe", "#10232a"),
    text_color=("gray30", "gray80")
)
thumbnail_label.grid(row=0, column=0, rowspan=4, padx=(0, 16), sticky="n")

titulo_video = ctk.CTkLabel(
    preview_content,
    text=t("video_title_placeholder"),
    wraplength=280,
    justify="left",
    anchor="w",
    font=("Arial", 18, "bold")
)
titulo_video.grid(row=0, column=1, sticky="w", pady=(6, 10))

canal_video = ctk.CTkLabel(
    preview_content,
    text=t("channel_placeholder"),
    anchor="w",
    font=("Arial", 13)
)
canal_video.grid(row=1, column=1, sticky="w", pady=4)

duracao_video = ctk.CTkLabel(
    preview_content,
    text=t("duration_placeholder"),
    anchor="w",
    font=("Arial", 13)
)
duracao_video.grid(row=2, column=1, sticky="w", pady=4)

status_video = ctk.CTkLabel(
    preview_content,
    text=t("status_waiting"),
    anchor="w",
    font=("Arial", 12),
    text_color=("gray35", "gray75")
)
status_video.grid(row=3, column=1, sticky="w", pady=(12, 0))


options_row = ctk.CTkFrame(main_card, fg_color="transparent")
options_row.pack(fill="x", padx=22, pady=(0, 14))

left_options = ctk.CTkFrame(options_row, corner_radius=18)
left_options.pack(side="left", fill="both", expand=True, padx=(0, 8))

right_options = ctk.CTkFrame(options_row, corner_radius=18)
right_options.pack(side="left", fill="both", expand=True, padx=(8, 0))

left_title = ctk.CTkLabel(
    left_options,
    text=t("download_type"),
    font=("Arial", 15, "bold")
)
left_title.pack(anchor="w", padx=16, pady=(14, 12))

tipo_frame = ctk.CTkFrame(left_options, fg_color="transparent")
tipo_frame.pack(anchor="w", padx=16, pady=(0, 14))

video_radio = ctk.CTkRadioButton(
    tipo_frame,
    text=t("video"),
    variable=tipo_var,
    value="video"
)
video_radio.pack(anchor="w", pady=6)

audio_radio = ctk.CTkRadioButton(
    tipo_frame,
    text=t("audio"),
    variable=tipo_var,
    value="audio"
)
audio_radio.pack(anchor="w", pady=6)

right_title = ctk.CTkLabel(
    right_options,
    text=t("quality_title"),
    font=("Arial", 15, "bold")
)
right_title.pack(anchor="w", padx=16, pady=(14, 12))

opcoes_container = ctk.CTkFrame(right_options, fg_color="transparent")
opcoes_container.pack(fill="x", padx=16, pady=(0, 14))

qualidade_video_label = ctk.CTkLabel(
    opcoes_container,
    text=t("video_quality"),
    font=("Arial", 13, "bold")
)
qualidade_video_menu = ctk.CTkOptionMenu(
    opcoes_container,
    values=[t("waiting_video")],
    height=38,
    corner_radius=12,
    fg_color=ACCENT,
    button_color=ACCENT_HOVER,
    button_hover_color="#168ea0"
)
qualidade_video_menu.set(t("waiting_video"))

qualidade_audio_label = ctk.CTkLabel(
    opcoes_container,
    text=t("audio_quality"),
    font=("Arial", 13, "bold")
)
qualidade_audio_menu = ctk.CTkOptionMenu(
    opcoes_container,
    values=["320", "192", "128"],
    height=38,
    corner_radius=12,
    fg_color=ACCENT,
    button_color=ACCENT_HOVER,
    button_hover_color="#168ea0"
)
qualidade_audio_menu.set("320")

rapido_checkbox = ctk.CTkCheckBox(
    opcoes_container,
    text=t("fast_download"),
    variable=rapido_var,
    checkbox_width=20,
    checkbox_height=20,
    corner_radius=6,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER
)

ToolTip(rapido_checkbox, lambda: t("fast_tooltip"))


def atualizar_opcoes():
    for widget in opcoes_container.winfo_children():
        widget.pack_forget()

    if tipo_var.get() == "video":
        qualidade_video_label.pack(anchor="w", pady=(0, 6))
        qualidade_video_menu.pack(fill="x")
        rapido_checkbox.pack(anchor="w", pady=(12, 0))

    elif tipo_var.get() == "audio":
        qualidade_audio_label.pack(anchor="w", pady=(0, 6))
        qualidade_audio_menu.pack(fill="x")


def ao_mudar_tipo():
    atualizar_opcoes()


video_radio.configure(command=ao_mudar_tipo)
audio_radio.configure(command=ao_mudar_tipo)


progress_card = ctk.CTkFrame(main_card, corner_radius=18)
progress_card.pack(fill="x", padx=22, pady=(0, 14))

progress_header = ctk.CTkFrame(progress_card, fg_color="transparent")
progress_header.pack(fill="x", padx=16, pady=(14, 8))

progress_title = ctk.CTkLabel(
    progress_header,
    text=t("progress_title"),
    font=("Arial", 15, "bold")
)
progress_title.pack(side="left")

progress_percent_label = ctk.CTkLabel(
    progress_header,
    text="0%",
    font=("Arial", 13, "bold"),
    text_color=ACCENT
)
progress_percent_label.pack(side="right")

progress_bar = ctk.CTkProgressBar(
    progress_card,
    width=620,
    height=16,
    corner_radius=10,
    progress_color=ACCENT
)
progress_bar.pack(fill="x", padx=16, pady=(0, 16))
progress_bar.set(0)


def atualizar_progresso(valor):
    def update():
        progress_bar.set(valor)
        progress_percent_label.configure(text=f"{int(valor * 100)}%")
    app.after(0, update)


action_row = ctk.CTkFrame(main_card, fg_color="transparent")
action_row.pack(fill="x", padx=22, pady=(0, 20))

botao = ctk.CTkButton(
    action_row,
    text=t("download_button"),
    command=lambda: iniciar_download(),
    width=240,
    height=46,
    corner_radius=14,
    fg_color=ACCENT,
    hover_color=ACCENT_HOVER,
    text_color="white",
    font=("Arial", 15, "bold")
)
botao.pack()


def atualizar_textos_interface():
    app_title.configure(text=t("app_title"))
    app_subtitle.configure(text=t("app_subtitle"))

    if ctk.get_appearance_mode() == "Dark":
        tema_btn.configure(text=t("theme_light"))
    else:
        tema_btn.configure(text=t("theme_dark"))

    url_label.configure(text=t("url_label"))
    url_entry.configure(placeholder_text=t("url_placeholder"))
    preview_title.configure(text=t("preview_title"))
    left_title.configure(text=t("download_type"))
    right_title.configure(text=t("quality_title"))
    qualidade_video_label.configure(text=t("video_quality"))
    qualidade_audio_label.configure(text=t("audio_quality"))
    rapido_checkbox.configure(text=t("fast_download"))
    progress_title.configure(text=t("progress_title"))
    botao.configure(text=t("download_button"))
    video_radio.configure(text=t("video"))
    audio_radio.configure(text=t("audio"))

    language_menu.configure(values=[t("language_pt"), t("language_en")])
    language_menu.set(t("language_pt") if idioma_atual.get() == "pt" else t("language_en"))

    if ultimo_info_video["titulo"]:
        titulo_video.configure(text=ultimo_info_video["titulo"])
    else:
        titulo_video.configure(text=t("video_title_placeholder"))

    if ultimo_info_video["canal"]:
        canal_video.configure(text=f"{t('channel_prefix')}{ultimo_info_video['canal']}")
    else:
        canal_video.configure(text=t("channel_placeholder"))

    if ultimo_info_video["duracao"] is not None:
        duracao_video.configure(text=f"{t('duration_prefix')}{formatar_duracao(ultimo_info_video['duracao'])}")
    else:
        duracao_video.configure(text=t("duration_placeholder"))

    if ultimo_info_video["thumb_ok"]:
        thumbnail_label.configure(text="")
    else:
        if ultimo_info_video["status_key"] == "status_check_link":
            thumbnail_label.configure(text=t("thumb_load_error"))
        else:
            thumbnail_label.configure(text=t("preview_wait_thumb"))

    status_video.configure(text=t(ultimo_info_video["status_key"]))

    if qualidade_video_menu.get() in [TEXTS["pt"]["waiting_video"], TEXTS["en"]["waiting_video"]]:
        qualidade_video_menu.configure(values=[t("waiting_video")])
        qualidade_video_menu.set(t("waiting_video"))

    atualizar_opcoes()


def mudar_idioma(escolha):
    if escolha == TEXTS["pt"]["language_pt"]:
        idioma_atual.set("pt")
    else:
        idioma_atual.set("en")

    atualizar_textos_interface()


language_menu.configure(command=mudar_idioma)
language_menu.set(t("language_pt"))


def carregar_video():
    url = url_var.get().strip()

    if not url:
        return

    if url == ultimo_url_carregado["url"]:
        return

    ultimo_info_video["status_key"] = "status_loading_video"
    status_video.configure(text=t("status_loading_video"))

    def thread():
        try:
            info = obter_info_video(url)
            resolucoes = info["resolucoes"]
            resolucoes_formatadas = [f"{r}p" for r in resolucoes] if resolucoes else [t("no_options")]

            thumb_url = info["thumbnail"]
            thumb = None

            if thumb_url:
                response = requests.get(thumb_url, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                img = img.resize((320, 180))
                thumb = ctk.CTkImage(light_image=img, dark_image=img, size=(320, 180))

            def update():
                ultimo_url_carregado["url"] = url
                ultimo_info_video["titulo"] = info["titulo"] or t("title_unavailable")
                ultimo_info_video["canal"] = info["canal"]
                ultimo_info_video["duracao"] = info["duracao"]
                ultimo_info_video["thumb_ok"] = thumb is not None
                ultimo_info_video["status_key"] = "status_video_loaded"

                qualidade_video_menu.configure(values=resolucoes_formatadas)
                qualidade_video_menu.set(resolucoes_formatadas[-1])

                atualizar_textos_interface()

                if thumb:
                    thumbnail_label.configure(image=thumb, text="")
                    thumbnail_label.image = thumb
                else:
                    thumbnail_label.configure(image=None, text=t("thumb_unavailable"))
                    thumbnail_label.image = None

                atualizar_opcoes()

            app.after(0, update)

        except Exception as e:
            mensagem = str(e)

            def update_erro():
                ultimo_info_video["titulo"] = None
                ultimo_info_video["canal"] = None
                ultimo_info_video["duracao"] = None
                ultimo_info_video["thumb_ok"] = False
                ultimo_info_video["status_key"] = "status_check_link"

                titulo_video.configure(text=t("status_invalid_video"))
                canal_video.configure(text=t("channel_placeholder"))
                duracao_video.configure(text=t("duration_placeholder"))
                status_video.configure(text=mensagem[:120])
                thumbnail_label.configure(image=None, text=t("thumb_load_error"))
                thumbnail_label.image = None
                qualidade_video_menu.configure(values=[t("waiting_video")])
                qualidade_video_menu.set(t("waiting_video"))
                progress_bar.set(0)
                progress_percent_label.configure(text="0%")
                atualizar_opcoes()

            app.after(0, update_erro)

    threading.Thread(target=thread, daemon=True).start()

def detectar_url(*args):
    url = url_var.get().strip()

    if carregamento_agendado["id"] is not None:
        app.after_cancel(carregamento_agendado["id"])

    if "youtube.com" in url or "youtu.be" in url:
        carregamento_agendado["id"] = app.after(700, carregar_video)


url_var.trace_add("write", detectar_url)


def iniciar_download():
    url = url_var.get().strip()
    tipo = tipo_var.get()
    rapido = rapido_var.get()

    if not url:
        ultimo_info_video["status_key"] = "status_paste_url"
        status_video.configure(text=t("status_paste_url"))
        return

    if tipo == "video":
        qualidade = qualidade_video_menu.get().replace("p", "")
        if qualidade in [t("waiting_video"), t("no_options")]:
            status_video.configure(text="Carregue um vídeo válido antes de baixar.")
            return

    elif tipo == "audio":
        qualidade = qualidade_audio_menu.get()
        rapido = False

    else:
        ultimo_info_video["status_key"] = "status_choose_type"
        status_video.configure(text=t("status_choose_type"))
        return

    progress_bar.set(0)
    progress_percent_label.configure(text="0%")
    ultimo_info_video["status_key"] = "status_starting_download"
    status_video.configure(text=t("status_starting_download"))
    botao.configure(state="disabled")

    def thread():
        try:
            pasta_saida = baixar_video(url, tipo, qualidade, rapido, atualizar_progresso)

            def sucesso():
                ultimo_info_video["status_key"] = "status_download_success"
                status_video.configure(text=f"{t('status_download_success')} Pasta: {pasta_saida}")
                botao.configure(state="normal")

            app.after(0, sucesso)

        except Exception as e:
            mensagem = str(e)

            def erro():
                ultimo_info_video["status_key"] = "status_download_error"
                status_video.configure(text=mensagem[:140])
                botao.configure(state="normal")

            app.after(0, erro)

    threading.Thread(target=thread, daemon=True).start()

def mostrar_popup_saida():
    if nao_mostrar_popup_saida.get():
        app.destroy()
        return

    if popup_saida_aberto["valor"]:
        return

    popup_saida_aberto["valor"] = True

    popup = ctk.CTkToplevel(app)
    popup.title("Before closing" if idioma_atual.get() == "en" else "Antes de sair")
    popup.geometry("420x260")
    popup.resizable(False, False)
    popup.transient(app)
    popup.grab_set()

    def ao_fechar_popup():
        popup_saida_aberto["valor"] = False
        popup.destroy()

    popup.protocol("WM_DELETE_WINDOW", ao_fechar_popup)

    card = ctk.CTkFrame(popup, corner_radius=18)
    card.pack(fill="both", expand=True, padx=18, pady=18)

    titulo_popup = ctk.CTkLabel(
        card,
        text=t("popup_title"),
        font=("Arial", 22, "bold")
    )
    titulo_popup.pack(pady=(18, 10))

    texto_popup = ctk.CTkLabel(
        card,
        text=t("popup_text"),
        justify="center",
        wraplength=320,
        font=("Arial", 13)
    )
    texto_popup.pack(pady=(0, 14))

    link_label = ctk.CTkLabel(
        card,
        text=GITHUB_URL,
        text_color=ACCENT,
        font=("Arial", 12, "underline"),
        cursor="hand2"
    )
    link_label.pack(pady=(0, 14))
    link_label.bind("<Button-1>", lambda e: abrir_github())

    checkbox_popup = ctk.CTkCheckBox(
        card,
        text=t("popup_checkbox"),
        variable=nao_mostrar_popup_saida,
        fg_color=ACCENT,
        hover_color=ACCENT_HOVER
    )
    checkbox_popup.pack(pady=(0, 16))

    botoes_frame = ctk.CTkFrame(card, fg_color="transparent")
    botoes_frame.pack(pady=(0, 10))

    def abrir_github_e_fechar():
        webbrowser.open(GITHUB_URL)
        popup.destroy()
        app.destroy()

    def fechar_popup_e_sair():
        popup.destroy()
        app.destroy()

    github_btn = ctk.CTkButton(
        botoes_frame,
        text=t("popup_open_github"),
        width=140,
        fg_color=ACCENT,
        hover_color=ACCENT_HOVER,
        command=abrir_github_e_fechar
    )
    github_btn.pack(side="left", padx=6)

    sair_btn = ctk.CTkButton(
        botoes_frame,
        text=t("popup_close_app"),
        width=140,
        fg_color="#64748b",
        hover_color="#475569",
        command=fechar_popup_e_sair
    )
    sair_btn.pack(side="left", padx=6)

    def liberar_flag(event=None):
        popup_saida_aberto["valor"] = False

    popup.bind("<Destroy>", liberar_flag)


atualizar_textos_interface()
app.protocol("WM_DELETE_WINDOW", mostrar_popup_saida)
app.mainloop()