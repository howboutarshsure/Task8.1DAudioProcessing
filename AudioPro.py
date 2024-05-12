import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# Setup the GPIO pin for the LED
LED_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize recognizer
r = sr.Recognizer()

# Define the audio files
audio_files = ['on.wav', 'off.wav']
current_file = 0

# Function to process audio file
def process_audio(file_path):
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        # Recognize speech using Google's speech recognition
        command = r.recognize_google(audio)
        print(f"Google Speech Recognition thinks you said: {command}")

        # Process command
        if "on" in command.lower():
            print("Turning the light ON.")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        elif "off" in command.lower():
            print("Turning the light OFF.")
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn LED off
        else:
            print("Command not recognized.")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

# Loop indefinitely switching between audio files
try:
    while True:
        print(f"Processing file: {audio_files[current_file]}")
        process_audio(audio_files[current_file])
        current_file = 1 - current_file  # Switch between 0 and 1
        time.sleep(1)  # Delay before processing the next file
finally:
    GPIO.cleanup()
