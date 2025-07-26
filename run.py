# run_both.py
import subprocess
import threading

def run_gradio():
    subprocess.run(["python", "app.py"])

def run_fastapi():
    subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    # Ejecuta Gradio en un hilo
    thread1 = threading.Thread(target=run_gradio, daemon=True)
    thread1.start()

    # Ejecuta FastAPI en el hilo principal
    run_fastapi()