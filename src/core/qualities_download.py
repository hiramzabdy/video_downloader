import yt_dlp
import os

def download_video_and_audio(url: str, output_folder: str = "downloads"):
    """
    Descarga un video con su mejor formato de audio disponible.
    
    :param url: URL del video de YouTube
    :param output_folder: Carpeta donde se guardará el archivo descargado
    """
    os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe
    
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

        # Mostrar opciones de formato disponibles
        print("Selecciona la calidad del video que deseas descargar:")

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

        # Ordenar los formatos según el índice del ordenamiento (1, 2, 3)
        sorted_formats.sort(key=lambda x: x[1])

        def get_vertical_resolution(resolution):
            """Extraer la resolución vertical de la cadena de resolución."""
            if 'x' in resolution:
                parts = resolution.split('x')
                return f"{parts[1]}p"
            return "Unknown"

        # Imprimir formatos ordenados y filtrados
        previous_codec_group = None

        for i, (fmt, order) in enumerate(sorted_formats):
            itag = str(fmt['format_id'])
            ext = fmt['ext']
            res = get_vertical_resolution(fmt.get('resolution'))
            fps = fmt.get('fps')
            size = fmt.get('filesize')
            size_mib = round(size / (2**20), 2) if isinstance(size, (int, float)) and size >= 0 else None
            
            codec_map = {
                'avc1': 'AVC - Stardard Quality, Highest Compatibility',
                'vp9': 'VP9 - Better Quality, Good Compatibility',
                'av01': 'AV1 - Highest Quality, Less Compatibility'
            }
            
            vcodec = fmt.get('vcodec').split('.')[0]  # Obtener solo la parte inicial del codec
            current_codec_group = codec_map.get(vcodec)
            
            if previous_codec_group != current_codec_group:
                print(f"\n{current_codec_group}")
                previous_codec_group = current_codec_group
            
            format_desc = f"Res: {res} {fps} FPS, Size: {size_mib} MiB, Codec: {current_codec_group}."
            
            print(f"[{i+1}] - {format_desc}")
            video_format_options[i + 1] = itag

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

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=EVbR7F2YgNQ"
    download_video_and_audio(test_url)