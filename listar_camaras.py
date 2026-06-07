#!/usr/bin/env python3
"""
Script para listar todas las cámaras web conectadas al PC
Con información detallada de cada dispositivo
"""

import cv2
import platform


def obtener_info_sistema():
    """Muestra información del sistema."""
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"OpenCV: {cv2.__version__}")
    print("-" * 60)


def obtener_propiedades_camara(cap):
    """Obtiene todas las propiedades disponibles de la cámara."""
    props = {
        # Dimensiones
        'Ancho': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'Alto': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),

        # FPS
        'FPS': int(cap.get(cv2.CAP_PROP_FPS)),

        # Formato
        'Formato': int(cap.get(cv2.CAP_PROP_FORMAT)),
        'Mode': int(cap.get(cv2.CAP_PROP_MODE)),

        # Codec
        'Codec (4 char)': int(cap.get(cv2.CAP_PROP_FOURCC)),

        # Brillo/Contraste/Saturación
        'Brillo': round(cap.get(cv2.CAP_PROP_BRIGHTNESS), 2),
        'Contraste': round(cap.get(cv2.CAP_PROP_CONTRAST), 2),
        'Saturación': round(cap.get(cv2.CAP_PROP_SATURATION), 2),
        'Hue': round(cap.get(cv2.CAP_PROP_HUE), 2),

        # Ganancia/Exposición
        'Ganancia': round(cap.get(cv2.CAP_PROP_GAIN), 2),
        'Exposición': round(cap.get(cv2.CAP_PROP_EXPOSURE), 2),

        # Enfoque
        'Enfoque': round(cap.get(cv2.CAP_PROP_FOCUS), 2),

        # Balance de blancos
        'Balance Blancos': round(cap.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U), 2),

        # Zoom
        'Zoom': round(cap.get(cv2.CAP_PROP_ZOOM), 2),

        # Buffer
        'Buffers': int(cap.get(cv2.CAP_PROP_BUFFERSIZE)),

        # Auto features
        'Auto Exposición': int(cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)),
        'Auto Enfoque': int(cap.get(cv2.CAP_PROP_AUTOFOCUS)),
        'Auto WB': int(cap.get(cv2.CAP_PROP_AUTO_WB)),
    }
    return props


def decode_fourcc(cc):
    """Decodifica el codec FOURCC a formato legible."""
    if cc == 0:
        return "N/A"
    return "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])


def obtener_nombre_backend(backend_name):
    """Devuelve descripción más legible del backend."""
    backends = {
        'MSMF': 'Microsoft Media Foundation (Windows)',
        'DSHOW': 'DirectShow (Windows)',
        'FFMPEG': 'FFmpeg',
        'V4L2': 'Video4Linux2 (Linux)',
        'AVFOUNDATION': 'AVFoundation (macOS)',
        'CAP_GSTREAMER': 'GStreamer',
        'INTEL_MFX': 'Intel Media SDK',
        'XINE': 'Xine (Linux)',
    }
    return backends.get(backend_name, backend_name)


def probar_resoluciones(cap):
    """Prueba diferentes resoluciones comunes."""
    resoluciones = [
        (640, 480),      # VGA
        (1280, 720),     # HD
        (1920, 1080),    # Full HD
        (320, 240),      # QVGA
        (800, 600),      # SVGA
        (2560, 1440),    # QHD
        (3840, 2160),    # 4K
    ]

    orig_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    orig_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    soportadas = []
    for w, h in resoluciones:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if actual_w == w and actual_h == h:
            soportadas.append(f"{w}x{h}")

    # Restaurar resolución original
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, orig_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, orig_h)

    return soportadas


def listar_camaras():
    """Lista todas las cámaras disponibles con información detallada."""
    obtener_info_sistema()
    print("Escaneando cámaras...")
    print("-" * 60)

    camaras_encontradas = []

    # Probar índices del 0 al 15
    for i in range(16):
        cap = cv2.VideoCapture(i, cv2.CAP_ANY)

        if cap.isOpened():
            ret, frame = cap.read()

            if ret:
                backend = cap.getBackendName()
                props = obtener_propiedades_camara(cap)
                soportadas = probar_resoluciones(cap)

                camaras_encontradas.append({
                    'indice': i,
                    'backend': backend,
                    'props': props,
                    'resoluciones': soportadas
                })

                print(f"\n[+] CÁMARA {i}")
                print(f"  Backend: {backend} ({obtener_nombre_backend(backend)})")
                print(f"  Resolución actual: {props['Ancho']}x{props['Alto']}")
                print(f"  FPS: {props['FPS']}")
                print(f"  Codec: {decode_fourcc(props['Codec (4 char)'])}")
                print(f"  Buffers: {props['Buffers']}")

                print(f"\n  Propiedades de imagen:")
                print(f"    Brillo: {props['Brillo']}")
                print(f"    Contraste: {props['Contraste']}")
                print(f"    Saturación: {props['Saturación']}")

                print(f"\n  Propiedades de cámara:")
                print(f"    Ganancia: {props['Ganancia']}")
                print(f"    Exposición: {props['Exposición']}")
                print(f"    Enfoque: {props['Enfoque']}")
                print(f"    Zoom: {props['Zoom']}")

                print(f"\n  Funciones automáticas:")
                print(f"    Auto Exposición: {'Sí' if props['Auto Exposición'] else 'No'}")
                print(f"    Auto Enfoque: {'Sí' if props['Auto Enfoque'] else 'No'}")
                print(f"    Auto WB: {'Sí' if props['Auto WB'] else 'No'}")

                print(f"\n  Resoluciones soportadas:")
                if soportadas:
                    print(f"    {', '.join(soportadas)}")
                else:
                    print(f"    Detectadas en ejecución")

            cap.release()

    print("\n" + "=" * 60)
    if camaras_encontradas:
        print(f"TOTAL: {len(camaras_encontradas)} cámara(s) encontrada(s)")
        print("\nÍndices disponibles:", ", ".join(str(c['indice']) for c in camaras_encontradas))
    else:
        print("No se encontraron cámaras conectadas.")
    print("=" * 60)

    return camaras_encontradas


def mostrar_camara(indice=0):
    """Muestra el stream de una cámara específica."""
    cap = cv2.VideoCapture(indice)

    if not cap.isOpened():
        print(f"Error: No se pudo abrir la cámara {indice}")
        return

    print(f"Mostrando cámara {indice}. Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(f'Cámara {indice}', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys

    # Si se pasa un índice como argumento, muestra esa cámara
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        indice = int(sys.argv[1])
        mostrar_camara(indice)
    else:
        listar_camaras()

        print("\nPara ver una cámara en tiempo real:")
        print("  python listar_camaras.py <indice>")
        print("  uv run listar_camaras.py <indice>")
