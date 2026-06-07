#!/usr/bin/env python3
"""
Script para listar todas las cámaras web conectadas al PC
"""

import cv2


def listar_camaras():
    """Lista todas las cámaras disponibles en el sistema."""
    print("Buscando cámaras conectadas...")
    print("-" * 50)

    camaras_encontradas = []

    # Probar índices del 0 al 10 (usualmente suficiente)
    for i in range(11):
        cap = cv2.VideoCapture(i)

        # Intentar abrir y leer un frame para verificar que la cámara funciona
        if cap.isOpened():
            ret, frame = cap.read()

            if ret:
                # Obtener información de la cámara
                ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                backend = cap.getBackendName()

                camaras_encontradas.append({
                    'indice': i,
                    'resolucion': f"{ancho}x{alto}",
                    'fps': fps,
                    'backend': backend
                })

                print(f"[+] Cámara {i}")
                print(f"  Resolución: {ancho}x{alto}")
                print(f"  FPS: {fps}")
                print(f"  Backend: {backend}")
                print()

            cap.release()

    print("-" * 50)

    if camaras_encontradas:
        print(f"Total de cámaras encontradas: {len(camaras_encontradas)}")
    else:
        print("No se encontraron cámaras conectadas.")

    return camaras_encontradas


if __name__ == "__main__":
    camaras = listar_camaras()
