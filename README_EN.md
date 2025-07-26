# Demo AI Interview
## OpenAI Whisper + Gemini + ChatGpt + FastAPI + Gradio

Este proyecto permite grabar audio, transcribirlo usando Whisper, generar preguntas técnicas aleatorias y validar respuestas usando modelos de OpenAI (GPT) y Gemini, todo a través de una API construida con FastAPI.

## Requisitos

- Python 3.13.3
- Las siguientes librerías (ver `requeriments.txt`):
  - openai
  - python-dotenv
  - sounddevice
  - scipy
  - keyboard
  - fastapi

## Instalación

1. Clona el repositorio y navega a la carpeta del proyecto.
2. Instala los requerimientos:

   ```sh
   pip install -r requeriments.txt
   ```

3. Configura las claves API en el archivo `.env` (ya incluido en el proyecto).

## Ejecución

1. Inicia el servidor FastAPI:

   ```sh
   python main.py
   ```

   El servidor estará disponible en `http://localhost:8000`.

2. Para grabar audio, ejecuta:

   ```sh
   python record-audio.py
   ```

   El archivo de audio se guardará en la carpeta `audio/` como `output.wav`.

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

## Ejemplo de uso (ver `pruebas.txt`)

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