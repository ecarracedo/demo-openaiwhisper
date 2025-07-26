import gradio as gr
import requests
import os
import subprocess

API_BASE = "http://localhost:8001"
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

pregunta_actual = ""

def obtener_pregunta(rol, modelo):
    global pregunta_actual
    endpoint = "/pregunta-random-gpt" if modelo == "GPT" else "/pregunta-random-gemini"
    res = requests.post(f"{API_BASE}{endpoint}", json={"rol": rol})
    if res.ok:
        pregunta_actual = res.json()["pregunta"]
        return pregunta_actual
    else:
        return "❌ Error al obtener pregunta"

def transcribir_y_verificar(audio_file, rol, modelo):
    global pregunta_actual

    if not pregunta_actual:
        return "⚠️ Primero obtené una pregunta."

    # Convertir a WAV si no lo está
    wav_path = os.path.join(AUDIO_DIR, "output.wav")
    subprocess.run(["ffmpeg", "-y", "-i", audio_file, wav_path], check=True)

    # Transcribir
    trans_res = requests.post(f"{API_BASE}/transcribe-audio/", json={
        "file_name": "output.wav",
        "folder": "audio",
        "role": rol,
        "question": pregunta_actual
    })

    if not trans_res.ok:
        return "❌ Error al transcribir"

    transcripcion = trans_res.json().get("transcription", "[Sin texto]")

    # Verificar
    endpoint = "/check-respuesta-gpt" if modelo == "GPT" else "/check-respuesta-gemini"
    verif_res = requests.post(f"{API_BASE}{endpoint}", json={
        "rol": rol,
        "pregunta": pregunta_actual,
        "respuesta": transcripcion
    })

    if not verif_res.ok:
        return "❌ Error al verificar respuesta"

    if modelo == "GPT":
        evaluacion = verif_res.json().get("respuesta_valida", "¿?")
    else:
        correcto = verif_res.json().get("correcta", 0)
        evaluacion = "✅ Correcta" if correcto else "❌ Incorrecta"

    return f"📄 Transcripción: {transcripcion}\n\n🧠 Evaluación: {evaluacion}"


with gr.Blocks() as demo:
    gr.Markdown("# 🧠 Evaluador Técnico por Voz")

    with gr.Row():
        rol = gr.Dropdown(["Data Science", "Backend", "DevOps"], label="Rol")
        modelo = gr.Radio(["GPT", "Gemini"], label="Modelo")

    pregunta_btn = gr.Button("🎲 Obtener pregunta")
    pregunta_output = gr.Textbox(label="Pregunta", interactive=False)
    pregunta_btn.click(fn=obtener_pregunta, inputs=[rol, modelo], outputs=pregunta_output)

    # 🎤 Audio grabado por usuario
    audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Grabá tu respuesta")

    # ✅ Resultado
    resultado = gr.Textbox(label="Resultado", lines=6)
    procesar_btn = gr.Button("✅ Transcribir y Evaluar")
    procesar_btn.click(fn=transcribir_y_verificar, inputs=[audio_input, rol, modelo], outputs=resultado)

demo.launch()
