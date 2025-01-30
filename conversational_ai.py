import speech_recognition as sr
import os
import together

#TOGETHER_API_KEY="50d44ded90930c29f77b6bea0f34c32da8be71304070db98d4e7689edccb4c87"

def setup_together_api():
    api_key = os.getenv("TOGETHER_API_KEY")  # Load the key manually
    if not api_key:
        raise ValueError("TOGETHER_API_KEY is not set. Set it in your environment variables.")
    
    together.api_key = "50d44ded90930c29f77b6bea0f34c32da8be71304070db98d4e7689edccb4c87"
    return together

def transcribe_speech():
    """Captures and transcribes user speech using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError:
        print("Could not request results, check your internet connection.")
        return None

def get_ai_response(client, prompt):
    """Sends transcribed text to AI model and returns the response."""
    try:
        response = client.completions.create(
            model="mistralai/mistral-7b-instruct",  
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error generating response:", str(e))
        return "Sorry, I couldn't process your request."

def main():
    """Main function to run the IELTS AI test simulation."""
    client = setup_together_api()
    print("Welcome to the IELTS Speaking Test Simulation!")
    
    questions = [
        "Tell me about yourself.",
        "Describe a place you would like to visit.",
        "What are the advantages and disadvantages of social media?"
    ]
    
    for question in questions:
        print("Examiner:", question)
        user_response = transcribe_speech()
        if user_response:
            ai_response = get_ai_response(client, "Evaluate this IELTS speaking response: " + user_response)
            print("AI Examiner Feedback:", ai_response)
    
if __name__ == "__main__":
    main()