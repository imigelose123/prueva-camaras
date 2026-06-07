#!/usr/bin/env python3
"""
Script para capturar una foto usando una cámara específica
"""

import cv2
import datetime
import os


def sacar_foto(indice_camara, nombre_salida=None):
    """
    Captura una foto de la cámara especificada

    Args:
        indice_camara: Índice de la cámara a usar
        nombre_salida: Nombre del archivo de salida (opcional)
    """
    # Crear carpeta output si no existe
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Inicializar cámara
    cap = cv2.VideoCapture(indice_camara)

    if not cap.isOpened():
        print(f"Error: No se pudo abrir la cámara {indice_camara}")
        return False

    print(f"Capturando foto de cámara {indice_camara}...")

    # Leer frame
    ret, frame = cap.read()

    if ret:
        # Generar nombre de archivo si no se proporciona
        if nombre_salida is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_salida = f"foto_{timestamp}.jpg"

        # Ruta completa en la carpeta output
        ruta_completa = os.path.join(output_dir, nombre_salida)

        # Guardar imagen
        cv2.imwrite(ruta_completa, frame)
        print(f"Foto guardada: {ruta_completa}")
        print(f"Resolución: {frame.shape[1]}x{frame.shape[0]}")

        cap.release()
        return True
    else:
        print("Error: No se pudo capturar el frame")
        cap.release()
        return False


if __name__ == "__main__":
    # DroidCam Source 3 es el índice 1
    INDICE_CAMARA = 1

    sacar_foto(INDICE_CAMARA)
