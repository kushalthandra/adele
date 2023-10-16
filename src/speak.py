import pyttsx3
import speech_recognition as sr

engine=pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()