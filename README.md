# IELTS Speaking Test Simulation Tool


## Getting started/ Overview

This tool simulates a real-time IELTS Speaking Test, allowing users to practice speaking English and receive performance assessments based on IELTS criteria such as fluency, pronunciation, grammar, and vocabulary. The tool integrates a Speech-to-Text API for real-time transcription and uses a conversational AI to simulate an IELTS examiner's responses. It provides detailed feedback and generates a PDF report at the end of the session.

## Features

Real-Time Conversation: Utilizes a Speech-to-Text API for real-time transcription and a conversational AI for examiner responses.

IELTS Scoring Simulation: Evaluates responses based on IELTS criteria:

Fluency & Coherence

Lexical Resource

Grammatical Range & Accuracy

Pronunciation

Session Types:

Practice Mode: Instant feedback for each response.

Test Mode: Full IELTS Speaking Test with 3 sections:

Part 1: Introduction

Part 2: Long Turn (Cue Card Activity)

Part 3: Two-Way Discussion

Custom Feedback: Provides corrected sentences, pronunciation tips, and vocabulary suggestions.

PDF Report: Generates a downloadable PDF report with scores and improvement recommendations.

## Requirements
Python 3.7 or higher

Vosk model for speech recognition

OpenAI API key

## Installation


Installation
Clone the repository:

bash
Copy
git clone https://github.com/Thendo-code/Task-1.git
cd task-1
Install dependencies:

bash
Copy
pip install sounddevice vosk openai fpdf
Set up environment variables:

Set your OpenAI API key as an environment variable:

bash
Copy
export OPENAI_API_KEY='your-api-key'
Download Vosk model:

Download a Vosk model from Vosk Models and place it in the project directory.

## Usage

Run the script with the path to the Vosk model:

bash
Copy
python ai.py --model-path "vosk-model"
Command-Line Arguments
--model-path: Path to the Vosk model directory (required).
***

# How It Works


Audio Input: The tool listens to the user's speech in real-time using the sounddevice library.

Speech-to-Text: The speech is transcribed using the Vosk model.

AI Response: The transcribed text is sent to the OpenAI API, which simulates an IELTS examiner's response.

Feedback: The tool provides feedback based on IELTS criteria and generates a PDF report.



## Code Structure

main.py: The main script that handles audio input, transcription, AI response, and feedback generation.

README.md: This file, providing an overview and instructions for the tool.

## Customization
LLM Selection: You can customize the LLM used by modifying the get_ai_response function in main.py.

Feedback Criteria: Adjust the feedback criteria in the provide_custom_feedback function.
## Challenges and Solutions
Real-Time Transcription: Ensuring minimal delay for a smooth conversation was challenging. Using the Vosk model and optimizing the audio input settings helped achieve near real-time performance.

Feedback Accuracy: The feedback accuracy depends on the AI model used. Fine-tuning the prompt and using a more advanced model can improve accuracy.

## Future Enhancements

Progress Tracking: Implement progress tracking over multiple sessions.

Multi-Language Support: Add support for feedback in multiple languages.

Cue Card Visuals: Enhance the user experience with visual cues for the cue card activity.
## Acknowledgments
Vosk for the speech recognition model.

OpenAI for the conversational AI.

FPDF for PDF generation.
## Contact
For any questions or issues, please open an issue on the GitHub repository or contact the maintainer directly.
My email address: thendolidala90@gmail.com

