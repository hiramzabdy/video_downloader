# **📌 Proyecto: Video Downloader**  
**Descripción:**  
Una aplicación con interfaz gráfica (GUI) desarrollada en **Python** con **PyQt6** para descargar videos de YouTube y otras plataformas. Soporta la descarga de solo audio y funciona en **Linux** y **Windows**.  

**Objetivos principales:**  
✔ Descarga de videos mediante `yt-dlp`.  
✔ Interfaz intuitiva con PyQt6.  
✔ Compatibilidad con Linux y Windows.  
✔ Empaquetado como AppImage (`.appimage`) en Linux y ejecutable portable (`.exe`) en Windows.  

---

## **📁 Estructura del Proyecto**  

```
video_downloader/
│── src/
│   ├── core/
│   │   ├── downloader.py  # Lógica de descarga de videos
│   │   ├── __init__.py  
│   │
│   ├── ui/
│   │   ├── main_window.py  # Interfaz gráfica (PyQt6)
│   │   ├── __init__.py  
│
├── downloads/  # Carpeta donde se guardan los videos descargados
│── requirements.txt  # Dependencias del proyecto
│── README.md  # Documentación del proyecto
│── .gitignore  # Archivos a ignorar en Git
```

---

## **⚙️ Tecnologías utilizadas**
- **Lenguaje:** Python 3  
- **Librerías principales:**
  - `PyQt6` → Para la interfaz gráfica  
  - `yt-dlp` → Para descargar videos  
  - `QThread` → Para evitar que la GUI se congele durante las descargas  
- **Sistema de gestión de paquetes:** `pip`  
- **Gestión del código:** `git` + `.gitignore`  
- **Distribución final:**
  - `.exe` portable en Windows (con `PyInstaller`)  
  - `.appimage` en Linux  
  - Instalación vía `apt` (futuro)  

---

## **🖥️ Estado actual del desarrollo**
✅ **Funcionalidad Base:**  
✔ Descarga de videos con `yt-dlp`.  
✔ Interfaz gráfica funcional.  
✔ Uso de hilos (`QThread`) para mantener la UI reactiva.  
✔ Las descargas se almacenan en `../downloads`.  

📌 **Próximos pasos:**  
- Mejorar la interfaz visual.  
- Agregar barra de progreso.  
- Implementar configuración de calidad de video/audio.  