import yt_dlp
import os
import re

def download_video_and_audio(url: str, output_folder: str = "downloads", audio_only: bool = False):
    """
    Descarga un video con su mejor formato de audio disponible.
    
    :param url: URL del video de YouTube
    :param output_folder: Carpeta donde se guardará el archivo descargado
    """
    # os.makedirs(output_folder, exist_ok=True) #Creates folder if it doesn't exist
    
    ydl_opts_info = {
        'format': 'best',
        'dump_single_json': True,
        'listformats': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl_info:
            video_info = ydl_info.extract_info(url, download=False) 
        
        formats = video_info.get('formats', [])
        video_format_options = {} #Used to select item to download from list
        sorted_formats = sort_formats(formats) #Sorts items by codec (avc, vp, av1) and res (lower to higher)

        print("Selecciona la calidad del video que deseas descargar:")
        codec_map = {
            'avc1': 'Codec: AVC - Stardard Quality, Highest Compatibility',
            'vp9': 'Codec: VP9 - Better Quality, Good Compatibility',
            'av01': 'Codec: AV1 - Highest Quality, Less Compatibility'
        }
        
        previous_codec_group = None

        #Prints each format and its details
        for i, (fmt, order) in enumerate(sorted_formats):
            itag = str(fmt['format_id'])
            ext = fmt['ext']
            res = get_vertical_resolution(fmt.get('resolution'))
            fps = fmt.get('fps')
            size = fmt.get('filesize')
            size_mib = round(size / (2**20), 2) if isinstance(size, (int, float)) and size >= 0 else None
            
            vcodec = fmt.get('vcodec').split('.')[0]  # Gets only initial part of the codec
            current_codec_group = codec_map.get(vcodec)
            
            # Prints header for each codec
            if previous_codec_group != current_codec_group:
                print(f"\n{current_codec_group}")
                previous_codec_group = current_codec_group
            
            format_desc = f"Res: {res} {fps} FPS, Size: {size_mib} MiB."
            
            print(f"[{i+1}] - {format_desc}")
            video_format_options[i + 1] = itag #Ties each format to an index, starting by 1

        while True:
            try:
                choice_video = int(input("Ingresa el número del formato de vídeo deseado: "))
                if choice_video in video_format_options.keys():
                    break
                else:
                    print("Opción no válida, intenta nuevamente.")
            except ValueError:
                print("Entrada no válida. Ingresa un número.")

        # Descargar el formato seleccionado de vídeo
        selected_video_format_id = video_format_options[choice_video]
        
        ydl_opts_download_video = {
            'format': f'{selected_video_format_id}+bestaudio/best',
            'outtmpl': os.path.join(output_folder, '%(title)s - %(height)sp.%(ext)s'),
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts_download_video) as ydl:
            ydl.download([url])

    except Exception as e:
        print(f"Error al descargar el video: {e}")
        return

def sort_formats(formats):
    # Filtrar los formatos en orden específico (avc1, vp9, av01)
    sorted_formats = []
    for fmt in formats:
        if  fmt['vcodec'] != 'none' and isinstance(fmt.get('filesize'), (int, float))      :
            vcodec = fmt.get('vcodec')
            if vcodec.startswith('avc1'):
                sorted_formats.append((fmt, 1))  # Ordenamiento por avc1
            elif vcodec.startswith('vp9'):
                sorted_formats.append((fmt, 2))  # Ordenamiento por vp9
            elif vcodec.startswith('av01'):
                sorted_formats.append((fmt, 3))  # Ordenamiento por av01
    sorted_formats.sort(key=lambda x: x[1]) # Ordenar los formatos según el índice del ordenamiento (1, 2, 3)
    return sorted_formats

def get_vertical_resolution(resolution):
    """Extraer la resolución vertical de la cadena de resolución."""
    if 'x' in resolution:
        parts = resolution.split('x')
        return f"{parts[1]}p"
    return "Unknown"

def is_valid_youtube_url(url: str) -> bool:
    """
    Verifica si la URL ingresada es un enlace válido de YouTube.
    Soporta URLs de youtube.com y youtu.be.
    
    :param url: URL a validar.
    :return: True si es un enlace válido, False en caso contrario.
    """
    # Patrón para URLs de YouTube. Se acepta tanto el formato completo como el acortado.
    youtube_regex = (
        r'^(https?://)?(www\.)?'
        r'((youtube\.com/(watch\?v=|embed/))|(youtu\.be/))'
        r'[\w-]{11}'
    )
    
    return re.match(youtube_regex, url) is not None

if __name__ == "__main__":
    while True:
        video_url = input("Ingresa el link al video de YouTube: ").strip()
        if is_valid_youtube_url(video_url):
            break
        else:
            print("El enlace ingresado no es un enlace válido de YouTube. Intenta nuevamente.")
    
    download_video_and_audio(video_url)