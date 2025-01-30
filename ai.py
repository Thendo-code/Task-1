import os
import queue
import sounddevice as sd
import vosk
import json
import openai
from fpdf import FPDF
import datetime
import argparse
import sys
import threading

# Queue for storing audio data
audio_queue = queue.Queue()

# Flag to indicate when to stop transcription
stop_transcription = False

# Callback function to store recorded audio
def callback(indata, frames, time, status):
    if status:
        print("Audio status:", status, flush=True)
    audio_queue.put(bytes(indata))

# Function to listen for Enter key press
def listen_for_enter():
    global stop_transcription
    input("Press Enter to stop recording...\n")
    stop_transcription = True

# Start streaming audio input and transcribe
def real_time_transcription():
    global stop_transcription
    try:
        model = vosk.Model(args.model_path)  # Use the model path from args
        print("Vosk model loaded successfully.")
    except Exception as e:
        print("Error loading Vosk model:", str(e))
        sys.exit(1)

    recognizer = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback, device=1):  # Replace 1 with your device ID
        print("Listening... Press Enter to stop.")
        full_text = ""
        
        # Start a thread to listen for Enter key press
        enter_thread = threading.Thread(target=listen_for_enter)
        enter_thread.start()

        while not stop_transcription:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print("You said:", text)
                    full_text += " " + text

        print("Recording stopped.")
        return full_text.strip()

# Get AI response using OpenAI API
def get_ai_response(prompt):
    """Sends transcribed text to OpenAI API and returns the response."""
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for API key
        print("Sending request to OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an IELTS examiner evaluating a speaking response."},
                {"role": "user", "content": "Evaluate this IELTS speaking response: " + prompt}
            ],
            max_tokens=150
        )
        print("OpenAI API response received.")
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print("Error generating response:", str(e))
        return "Sorry, I couldn't process your request."

# Custom feedback for user response
def provide_custom_feedback(ai_response):
    """Provides custom feedback based on the AI response."""
    feedback = {
        "Fluency & Coherence": "Your response shows good fluency and coherence. Try to minimize pauses and maintain a logical flow.",
        "Lexical Resource": "You used a wide range of vocabulary. To further improve, try incorporating idiomatic expressions.",
        "Grammatical Range & Accuracy": "Your grammar is accurate. Focus on using complex sentences to showcase your skills.",
        "Pronunciation": "Your pronunciation is clear. Pay attention to the intonation for better expression."
    }
    # Dynamic adjustments based on AI response
    if "grammar" in ai_response.lower():
        feedback["Grammatical Range & Accuracy"] = "Your grammar needs improvement. Focus on subject-verb agreement and sentence structure."
    return feedback

# Generate PDF Report
def generate_pdf_report(all_feedback, user_responses):
    """Generates a PDF report for the IELTS practice session."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, txt="IELTS Speaking Test Simulation Report", ln=True, align='C')

    # Date and Time
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    # Feedback Section
    pdf.cell(200, 10, txt="Feedback:", ln=True, align='L')
    for question, feedback in all_feedback.items():
        pdf.cell(200, 10, txt=f"Question: {question}", ln=True, align='L')
        for key, value in feedback.items():
            pdf.multi_cell(0, 10, txt=f"{key}: {value}", align='L')  # Use multi_cell to wrap text

    # User Responses
    pdf.cell(200, 10, txt="User Responses:", ln=True, align='L')
    for question, response in user_responses.items():
        pdf.multi_cell(0, 10, txt=f"{question}: {response}", align='L')  # Use multi_cell to wrap text

    # Save PDF
    pdf_output_path = "IELTS_Speaking_Test_Report.pdf"
    pdf.output(pdf_output_path)
    print(f"Report saved as {pdf_output_path}")

def main():
    """Main function to run the IELTS AI test simulation."""
    print("Welcome to the IELTS Speaking Test Simulation!")
    
    questions = [
        "Hello, how are you?",
        "Tell me about yourself.",
        "Describe a place you would like to visit.",
    ]

    user_responses = {}
    all_feedback = {}

    for question in questions:
        print("Examiner:", question)
        try:
            user_response = real_time_transcription()
        except Exception as e:
            print("Error during transcription:", str(e))
            user_response = ""
        
        if user_response:
            ai_response = get_ai_response(user_response)
            user_responses[question] = user_response
            print("AI Examiner Feedback:", ai_response)
            feedback = provide_custom_feedback(ai_response)
            all_feedback[question] = feedback
            for key, value in feedback.items():
                print(f"{key}: {value}")

    # Generate PDF report
    generate_pdf_report(all_feedback, user_responses)

# Parse command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IELTS Speaking Test Simulation")
    parser.add_argument(
        "--model-path",
        type=str,
        required=True,
        help="Path to the Vosk model directory"
    )
    args = parser.parse_args()

    main()
    