import yt_dlp
import os

def download_video(url: str, output_folder: str = "downloads", audio_only: bool = False):
    """
    Descarga un video de YouTube en la mejor calidad disponible.
    
    :param url: URL del video de YouTube
    :param output_folder: Carpeta donde se guardará el archivo descargado
    :param audio_only: Si es True, descarga solo el audio
    """
    os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe
    
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'format': 'bestaudio' if audio_only else 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if audio_only else []
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Descarga completada.")
    except Exception as e:
        print(f"Error al descargar el video: {e}")

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=EVbR7F2YgNQ"
    download_video(test_url, audio_only=False)