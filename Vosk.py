import queue
import sounddevice as sd
import vosk
import json
import os
import threading
import tkinter as tk


# Define the model path
MODEL_PATH = r"C:\Users\thend\Task_1\vosk-model"

# Check if the model path exists
if not os.path.exists(MODEL_PATH):
    print(f"Model path does not exist: {MODEL_PATH}")
else:
    print(f"Model path found: {MODEL_PATH}")

# Attempt to load the Vosk model
try:
    model = vosk.Model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Queue for storing audio data
audio_queue = queue.Queue()

# Flag to control the transcription loop
transcribing = True

# Callback function to store recorded audio
def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_queue.put(bytes(indata))

# Start streaming audio input and transcribe
def real_time_transcription():
    global transcribing

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        recognizer = vosk.KaldiRecognizer(model, 16000)
        print("Listening...")

        while transcribing:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print("You said:", result.get("text", ""))

# Function to start the transcription in a separate thread
def start_transcription():
    transcription_thread = threading.Thread(target=real_time_transcription)
    transcription_thread.start()

# Function to stop the transcription
def stop_transcription():
    global transcribing
    transcribing = False
    print("Transcription stopped.")

# Create the Tkinter window
window = tk.Tk()
window.title("Real-Time Transcription")

# Create a button to start transcription
start_button = tk.Button(window, text="Start Transcription", command=start_transcription)
start_button.pack(pady=10)

# Create a button to stop transcription
stop_button = tk.Button(window, text="Stop Transcription", command=stop_transcription)
stop_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()


