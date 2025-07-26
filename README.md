# Demo Entrevista IA
## OpenAI + Gemini + GhatGPT + Whisper + FastAPI + Gradio

Este proyecto permite grabar audio, transcribirlo usando Whisper, generar preguntas técnicas aleatorias y validar respuestas usando modelos de OpenAI (GPT) y Gemini, todo a través de una API construida con FastAPI e interface Gradio.

## Requisitos

- Python 3.13.3
- Instalar las siguientes librerías (ver `requeriments.txt`)

## Instalación

1. Clona el repositorio y navega a la carpeta del proyecto.
2. Instala los requerimientos:

   ```sh
   pip install -r requeriments.txt
   ```

3. Crear un archivo `.env` con las siguiente variables:

   ```
   GEMINI_API_KEY='APIKEY-GEMINI'
   OPENAI_API_KEY= 'API-KEY-OPENAI'
   ```

4. Para usar `Whisper open-source` y grabar audio con `sounddevice + scipy`, necesitás instalar algunas dependencias del sistema operativo (Linux) además de los paquetes de Python:

   ```sh
   sudo apt update
   sudo apt install ffmpeg portaudio19-dev python3-pyaudio libsndfile1
   ```
   - **ffmpeg:** requerido por Whisper para manejar archivos de audio.
   - **portaudio19-dev** y **libsndfile1:** necesarios para que sounddevice funcione correctamente.

## Ejecución

1. ### Inicia el servidor FastAPI y Gradio Simultaneamente:

   ```sh
   python run.py
   ```

   * FastApi estará disponible en `http://localhost:8001`.
   * Gradio estara disponible en `http://localhost:7860`

2. ### Whisper: 

   Whisper se instalo localmente en el proyeco, por lo que el modelo se carga automáticamente al iniciar el servidor FastAPI con esta línea:

   ```python
   model = whisper.load_model("base")
   ```
   🔁 Esto significa que:
   - Se descarga una sola vez la primera vez que lo usás.
   - Luego queda cacheado en tu sistema (`~/.cache/whisper`) y se reutiliza cada vez que se arranca el servidor.

3. ### Para grabar audio sin Gradio, ejecuta:

   ```sh
   python record-audio.py
   ```

   El archivo de audio se guardará en la carpeta `audio/` como `ouput.wav`.

## Endpoints principales

- `/pregunta-random-gpt`  
  Genera una pregunta técnica aleatoria usando GPT para un rol específico.

- `/pregunta-random-gemini`  
  Genera una pregunta técnica aleatoria usando Gemini para un rol específico.

- `/transcribe-audio`  
  Transcribe el audio grabado y devuelve el texto.

- `/check-respuesta-gemini`  
  Valida si una respuesta es correcta usando Gemini.

- `/check-respuesta-gpt`  
  Valida si una respuesta es correcta usando GPT.

## Ejemplo de uso (ver `pruebas.txt`) sin Gradio

1. **Obtener una pregunta random**  
   Usa `/pregunta-random-gpt` o `/pregunta-random-gemini` con el rol deseado.

2. **Responder en audio**  
   Graba tu respuesta ejecutando `record-audio.py`. El audio se guarda en `audio/output.wav`.

3. **Transcribir el audio**  
   Usa el endpoint `/transcribe-audio` pasando el nombre del archivo, carpeta, rol y pregunta.

4. **Chequear la respuesta**  
   Usa `/check-respuesta-gemini` o `/check-respuesta-gpt` pasando el rol, pregunta y la transcripción como respuesta.


Consulta el archivo [`pruebas.txt`](pruebas.txt) para ejemplos de payloads y pasos detallados.

---

**Autor:**  
Proyecto demo para entrevistas técnicas con IA.
Desarrollado por Emiliano Carracedo | ecarracedo@gmail.com