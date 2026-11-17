import yt_dlp
url = input("Enter your video link: ").strip()

# Settings for the downloader.
ydl_opts = {
    # Prefer audio-only; otherwise use the best combined format.
    "format": "bestaudio/best",
     # Name the file using the video's title and file extension.
    "outtmpl": "%(title)s.%(ext)s",
    "noplaylist": True,

    # Convert the downloaded audio to MP3 using FFmpeg.
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
    }],
}
# Create a downloader object and download the supplied URL.
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Download compelete")