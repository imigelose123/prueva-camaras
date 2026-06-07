# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) cuando trabaja con código en este repositorio.

## Resumen del Proyecto

Script simple de Python para listar todas las cámaras conectadas al PC (webcams, cámaras virtuales, fuentes de cámaras IP). Usa OpenCV para la detección de cámaras y FFmpeg para obtener los nombres de los dispositivos.

## Comandos de Desarrollo

```bash
# Instalar/restaurar dependencias
uv sync
uv pip install opencv-python

# Ejecutar el script de listado de cámaras
uv run listar_camaras.py
```

## Arquitectura

**listar_camaras.py** - Script principal que:
1. Llama a FFmpeg mediante subprocess para obtener los nombres de los dispositivos de cámara (DirectShow en Windows)
2. Escanea los índices 0-15 usando OpenCV VideoCapture para detectar las cámaras disponibles
3. Mapea los nombres de FFmpeg a los índices de OpenCV y muestra los resultados

**Integración con FFmpeg**: El script usa `ffmpeg -list_devices true -f dshow -i dummy` y analiza stderr con regex para extraer los nombres de las cámaras. FFmpeg debe estar instalado en el sistema.

**Dependencias**:
- opencv-python: Captura de cámara
- pywin32: API de Windows (instalado pero no utilizado actualmente)
