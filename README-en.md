# YouTube Downloader

Desktop application for downloading YouTube videos and audio with a modern graphical interface, multiple quality options, video preview, progress bar, and theme/language switching.

## Preview

The application allows you to:

- paste a YouTube video link
- automatically load thumbnail, title, channel and duration
- choose between downloading video or audio
- select available quality options
- use fast download mode
- track download progress in real time
- switch between light and dark mode
- switch language between Portuguese and English

## Features

### Video Download
- Download videos in multiple resolutions
- Automatic detection of available video qualities
- FFmpeg support for merging audio and video
- Optional fast download mode

### Audio Download
- Convert to MP3
- Select audio quality

### Graphical Interface
- Interface built with CustomTkinter
- Video thumbnail preview
- Display of title, channel and duration
- Download progress bar
- Light/Dark theme toggle
- Multi-language support

### Extras
- Exit popup with link to the GitHub repository
- Tooltip explaining fast download mode

## Technologies Used

- Python
- CustomTkinter
- yt-dlp
- FFmpeg
- Requests
- Pillow

## Project Structure

```bash
Video Downloader/
├── app.py
├── downloader.py
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
├── downloads/
└── README.md
