import yt_dlp
import os

def download_video(url: str, output_folder: str = "downloads", audio_only=False):
    """
    Descarga un video de YouTube permitiendo que el usuario seleccione la opción de descarga.
    
    :param url: URL del video de YouTube
    :param output_folder: Carpeta donde se guardará el archivo descargado
    :param audio_only: Si es True, solo muestra opciones para descargar el audio
    """
    os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe

    def print_formats(formats):
        # Cabecera de la tabla
        header = f"{'ID':<10} {'Resolución':<20} {'Tamaño (MiB)':<15} {'Codec de Video':<30} {'Extensión':<10}"
        print(header)
        print("-" * len(header))
        
        # Imprimir los formatos relevantes en formato de tabla
        for fmt in formats:
            if not audio_only or 'audio' in fmt['format']:
                ext = fmt.get('ext', '')
                vcodec = fmt.get('vcodec', '')

                codec_match = (
                    (not audio_only and ext == 'mp4') or
                    (audio_only and ext == 'm4a')
                )

                if codec_match:
                    # Filtrar por codecs VP9 y AV1, incluyendo sus variaciones
                    vp9_variations = ['vp9', 'vp09']
                    av1_variations = ['av01']

                    codec_is_vpx_or_av1 = any(vcodec.startswith(var) for var in vp9_variations + av1_variations)

                    if codec_is_vpx_or_av1:
                        resolution = fmt.get('resolution', '-')
                        size_mb = round(fmt.get('filesize_approx', fmt.get('filesize')) / (1024 * 1024), 2) if fmt.get('filesize_approx') else '-'
                        print(f"{fmt['format_id']:<10} {resolution:<20} {size_mb:<15.2} {vcodec:<30} {ext:<10}")

    ydl_opts = {
        'listformats': True,
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        
        print_formats(formats)

        # Solicitar al usuario que elija una opción por ID
        selected_format_id = input("Introduce el ID del formato de descarga que deseas: ")
    
        try:
            with yt_dlp.YoutubeDL() as ydl:
                ydl.params['format'] = selected_format_id
                ydl.download([url])
            print("Descarga completada.")
        except Exception as e:
            print(f"Error al descargar el video con ID {selected_format_id}: {e}")

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=EVbR7F2YgNQ"
    download_video(test_url, audio_only=False)
