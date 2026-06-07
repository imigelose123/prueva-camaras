#!/usr/bin/env python3
"""
Script para listar todas las cámaras web conectadas al PC
"""

import cv2
import subprocess
import re


def obtener_nombres_camaras_ffmpeg():
    """Obtiene nombres de cámaras usando FFmpeg DirectShow."""
    nombres = {}

    try:
        result = subprocess.run(
            ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy'],
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        output = result.stderr
        pattern = r'\[in#0 @ [0-9a-f]+\]\s+"([^"]+)"\s+\(video\)'
        matches = re.findall(pattern, output)

        for idx, nombre in enumerate(matches):
            nombres[idx] = nombre

    except FileNotFoundError:
        print("(FFmpeg no encontrado)")
    except Exception:
        pass

    return nombres


def listar_camaras():
    """Lista todas las cámaras con sus nombres."""
    print("Escaneando cámaras...\n")

    # Obtener nombres con FFmpeg
    nombres_camaras = obtener_nombres_camaras_ffmpeg()

    camaras_encontradas = []

    # Buscar cámaras disponibles
    for i in range(16):
        cap = cv2.VideoCapture(i, cv2.CAP_ANY)

        if cap.isOpened():
            ret, frame = cap.read()

            if ret:
                nombre = nombres_camaras.get(i, f"Cámara {i}")
                camaras_encontradas.append((i, nombre))
                print(f"- CAMARA {i} -> Nombre: {nombre}")

            cap.release()

    print(f"\nTotal: {len(camaras_encontradas)} cámara(s)")
    return camaras_encontradas


if __name__ == "__main__":
    listar_camaras()
