from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import openai
import os
import whisper
from dotenv import load_dotenv



load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Cargar el modelo Whisper
model = whisper.load_model("base")  # podés usar "small", "medium", etc.

class AudioRequest(BaseModel):
    file_name: str  # ej: "output.wav"
    folder: str     # ej: "audio"
    role: str       # ej: "Data Science"
    question: str   # ej: "¿Qué es el overfitting?"

class RolRequest(BaseModel):
    rol: str

class CheckResponse(BaseModel):
    rol: str
    pregunta: str
    respuesta: str

@app.post("/procesar-audio")
def procesar_audio(request: AudioRequest):
    ruta = os.path.join(request.folder, request.filename)

    if not os.path.exists(ruta):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    # Acá iría la lógica de procesamiento (transcripción, análisis, etc.)
    return {
        "message": "Archivo encontrado",
        "ruta": ruta
    }

@app.post("/pregunta-random-gpt")
def obtener_pregunta_random(request: RolRequest):
    prompt = (
        f"Genera una sola pregunta técnica aleatoria que se le pueda hacer a un postulante para el rol de {request.rol}. "
        f"No incluyas la respuesta, solo la pregunta. Una pregunta simple sin desarrollo adicional."
        f"Tampoco incluyas que describen escenarios o situaciones complejas, solo una pregunta directa."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # o "gpt-3.5-turbo" si no tenés acceso a gpt-4
            messages=[
                {"role": "system", "content": "Eres un entrevistador técnico de IT."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        pregunta = response.choices[0].message.content.strip()
        return {"rol": request.rol, "pregunta": pregunta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pregunta-random-gemini")
async def pregunta_random_gemini(request: RolRequest):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash', temperature=0)

    """
    Genera texto usando el modelo Gemini AI basado en un prompt.
    """
    prompt = (
        f"Genera una sola pregunta técnica aleatoria que se le pueda hacer a un postulante para el rol de {request.rol}. "
        f"No incluyas la respuesta, solo la pregunta. Una pregunta simple sin desarrollo adicional."
        f"Tampoco incluyas que describen escenarios o situaciones complejas, solo una pregunta directa."
    )

    try:
        response = model.generate_content(prompt)
        # Puedes querer procesar la respuesta más a fondo, por ejemplo,
        # acceder a response.text o response.candidates[0].content.parts[0].text
        return {"rol": request.rol, "pregunta": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API de Gemini: {str(e)}")
    
@app.post("/transcribe-audio/")
def transcribe_audio(data: AudioRequest):
    audio_path = os.path.join(data.folder, data.file_name)

    if not os.path.isfile(audio_path):
        return {"error": f"Archivo no encontrado: {audio_path}"}

    try:
        result = model.transcribe(audio_path)
        transcription = result["text"]
    except Exception as e:
        return {"error": f"Error al transcribir: {str(e)}"}

    return {
        "role": data.role,
        "question": data.question,
        "transcription": transcription
    }

@app.post("/check-respuesta-gemini")
async def check_respuesta_gemini(request: CheckResponse):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash', temperature=0)

    """
    Genera texto usando el modelo Gemini AI basado en un prompt.
    """

    prompt = (
        f"Necesito verificar si la respuesta para el rol {request.rol} es correcta. "
        f"Pregunta: {request.pregunta}."
        f" Respuesta: {request.respuesta}. "
        f"¿Es correcta la respuesta? Responde con 'Sí' o 'No'. " 
    )

    try:
        response = model.generate_content(prompt)
        # Puedes querer procesar la respuesta más a fondo, por ejemplo,
        # acceder a response.text o response.candidates[0].content.parts[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al llamar a la API de Gemini: {str(e)}")
    
    if response.text.strip().lower() == "sí":
        return {"rol": request.rol,
                "pregunta": request.pregunta,
                "respuesta": request.respuesta,
                "correcta": 1
                }
              
    else:
          return {"rol": request.rol,
                "pregunta": request.pregunta,
                "respuesta": request.respuesta,
                "correcta": 0
                }

@app.post("/check-respuesta-gpt")
async def check_respuesta_gpt(request: CheckResponse):
    prompt = (
        f"Necesito verificar si la respuesta para el rol {request.rol} es correcta. "
        f"Pregunta: {request.pregunta} "
        f"Respuesta: {request.respuesta} "
        f"¿Es correcta la respuesta? Responde con 'Sí' o 'No'."
    )

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un evaluador técnico de entrevistas de IT. Responde solo con 'Sí' o 'No'."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=5
        )

        respuesta = completion.choices[0].message.content.strip()
        return {
            "rol": request.rol,
            "pregunta": request.pregunta,
            "respuesta_usuario": request.respuesta,
            "respuesta_valida": respuesta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)


