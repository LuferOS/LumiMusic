# 🎵 LumiMusic

<div align="center">

  ![Kotlin](https://img.shields.io/badge/Kotlin-B125EA?style=for-the-badge&logo=kotlin&logoColor=white)
  ![Jetpack Compose](https://img.shields.io/badge/Jetpack%20Compose-4285F4?style=for-the-badge&logo=android&logoColor=white)
  ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
  
  ![GitHub Repo stars](https://img.shields.io/github/stars/LuferOS/LumiMusic?style=for-the-badge&color=ffdd00)
  ![GitHub all releases](https://img.shields.io/github/downloads/LuferOS/LumiMusic/total?style=for-the-badge&color=00e676)

</div>

**LumiMusic** es un reproductor y descargador de música avanzado para Android, desarrollado 100% en Kotlin utilizando Jetpack Compose. Destaca por su alto nivel de personalización y una interfaz fluida. 

La aplicación está impulsada bajo el capó por **AlyaCore**, una potente API que actúa como motor de obtención y procesamiento de audio.

## ✨ Características Principales

*   **🎧 Potenciado por AlyaCore API:** Integración de motor dual automático para buscar, escuchar y descargar música utilizando los catálogos de Spotify y YouTube (el motor de descarga/reproducción es seleccionable desde el perfil).
*   **🎨 Personalización Extrema de UI:**
    *   **Color dinámico adaptativo** que se ajusta a la carátula de la canción actual.
    *   Temas personalizables con colores de acento (Cyan, Magenta, Lime, Naranja) y bordes de neón.
    *   Cambio de tipografía de la interfaz (Default, Serif, Monospace, Cursiva).
*   **🎛️ Audio FX y Ecualizador:** Control total sobre la velocidad de reproducción (Playback Speed), el tono de la canción (Pitch) y un ecualizador integrado para una experiencia auditiva a medida.
*   **🎶 Transiciones de Audio:** Soporte avanzado para reproducción sin pausas (*Gapless*) y transiciones suaves entre pistas (*Crossfade*).
*   **📊 Visualizadores de Espectro:** Animaciones en la pantalla de inicio con estilos configurables (Ondas, Bloques y Barras) y colores personalizados.
*   **📱 Arquitectura Moderna:** Construida completamente con Jetpack Compose, ofreciendo una experiencia responsiva, animaciones fluidas y soporte para modo oscuro.

## 📸 Capturas de Pantalla

*(Nota: Recuerda subir tus capturas a una carpeta `/assets` en tu repositorio para que se visualicen correctamente)*

<div align="center">
  <img src="assets/463764.jpg" width="220" alt="Biblioteca LumiMusic"/>
  <img src="assets/463778.jpg" width="220" alt="Búsqueda"/>
  <img src="assets/463780.jpg" width="220" alt="Resultados de Búsqueda"/>
  <img src="assets/463772.jpg" width="220" alt="Configuración y Personalización"/>
</div>

## 🛠️ Tecnologías Utilizadas

*   **Frontend (App):** Kotlin, Jetpack Compose, Material Design 3.
*   **Backend / API (AlyaCore):** Python & Shell (Gestión de los motores de descarga, extracción y automatización de metadatos).

## 🚀 Instalación y Compilación

1.  Clona este repositorio:
    ```bash
    git clone [https://github.com/LuferOS/LumiMusic.git](https://github.com/LuferOS/LumiMusic.git)
    ```
2.  Abre el proyecto en **Android Studio**.
3.  Espera a que Gradle sincronice todas las dependencias.
4.  Asegúrate de tener configurada la conexión a la API de **AlyaCore**.
5.  Compila y ejecuta la aplicación en tu emulador o dispositivo físico.

## 👨‍💻 Autor

Desarrollado por **LuferOS**
API: api.alyacore.xyz
