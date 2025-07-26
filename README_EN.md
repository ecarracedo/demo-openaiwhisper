
# AI Interview Demo
## OpenAI + Gemini + ChatGPT + Whisper + FastAPI + Gradio

This project allows you to record audio, transcribe it using Whisper, generate random technical questions, and validate answers using OpenAI (GPT) and Gemini models, all through an API built with FastAPI and a Gradio interface.

## Requirements

- Python 3.13.3
- Install the following libraries (see `requeriments.txt`)

## Installation

1. Clone the repository and navigate to the project folder.
2. Install the requirements:

   ```sh
   pip install -r requeriments.txt
   ```

3. Create a `.env` file in the root directory with the following variables:

   ```
   GEMINI_API_KEY='APIKEY-GEMINI'
   OPENAI_API_KEY='API-KEY-OPENAI'
   ```

4. To use `open-source Whisper` and record audio with `sounddevice + scipy`, you need to install some OS-level dependencies (Linux) in addition to the Python packages:

   ```sh
   sudo apt update
   sudo apt install ffmpeg portaudio19-dev python3-pyaudio libsndfile1
   ```
   - **ffmpeg:** required by Whisper to handle audio files.
   - **portaudio19-dev** and **libsndfile1:** needed for sounddevice to work correctly.

## Running

1. ### Start FastAPI and Gradio server simultaneously:

   ```sh
   python run.py
   ```

   * FastAPI will be available at `http://localhost:8001`.
   * Gradio will be available at `http://localhost:7860`.

2. ### Whisper:

   Whisper is installed locally in the project, so the model loads automatically when the FastAPI server starts using this line:

   ```python
   model = whisper.load_model("base")
   ```
   🔁 This means:
   - The model is downloaded only once the first time you use it.
   - It is then cached in your system (`~/.cache/whisper`) and reused every time the server is restarted.

3. ### To record audio without Gradio, run:

   ```sh
   python record-audio.py
   ```

   The audio file will be saved in the `audio/` folder as `output.wav`.

## Main Endpoints

- `/pregunta-random-gpt`  
  Generates a random technical question using GPT for a specific role.

- `/pregunta-random-gemini`  
  Generates a random technical question using Gemini for a specific role.

- `/transcribe-audio`  
  Transcribes the recorded audio and returns the text.

- `/check-respuesta-gemini`  
  Validates if a response is correct using Gemini.

- `/check-respuesta-gpt`  
  Validates if a response is correct using GPT.

## Usage Example (see `pruebas.txt`) without Gradio

1. **Get a random question**  
   Use `/pregunta-random-gpt` or `/pregunta-random-gemini` with the desired role.

2. **Answer by audio**  
   Record your answer by running `record-audio.py`. The audio is saved as `audio/output.wav`.

3. **Transcribe the audio**  
   Use the `/transcribe-audio` endpoint providing the filename, folder, role, and question.

4. **Check the answer**  
   Use `/check-respuesta-gemini` or `/check-respuesta-gpt` providing the role, question, and the transcribed answer.

Check the [`pruebas.txt`](pruebas.txt) file for example payloads and detailed steps.

---

**Author:**  
Demo project for AI-powered technical interviews.  
Developed by Emiliano Carracedo | ecarracedo@gmail.com
