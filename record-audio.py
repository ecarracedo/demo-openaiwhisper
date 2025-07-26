import sounddevice as sd
from scipy.io.wavfile import write
import time
import os

def record_audio(filename='output.wav', carpeta='audio'):
    input("Presiona Enter para comenzar a grabar...")
    print("Grabando... Presione Enter para detener la grabación.")    
    start_time = time.time()
    ruta_completa = os.path.join(carpeta, filename)

    fs = 44100  # Frecuencia de muestreo
    channels = 2
    duracion_maxima = 300  # segundos (5 minutos máx)

    # Empieza a grabar un buffer largo
    recording = sd.rec(int(fs * duracion_maxima), samplerate=fs, channels=channels, dtype='int16')

    try:
        input("Presiona Enter para detener la grabación...")
        sd.stop()
        end_time = time.time()
    finally:
        duration = end_time - start_time
        print(f"Duración de la grabación: {duration:.2f} segundos")

        # Recortar la grabación hasta la duración real
        recording_cortado = recording[:int(duration * fs)]
        write(ruta_completa, fs, recording_cortado)
        print(f"Audio guardado en {ruta_completa}")

record_audio()
