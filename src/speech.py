import speech_recognition as sr

def indentify_speech():
    recog=sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        recog.adjust_for_ambient_noise(source)
        try:
            audio=recog.listen(source)
            print("audio recording completed")
            print(audio)
            txt=recog.recognize_google(audio)
            #print(f"Transcription:{txt}")
        except Exception as e:
            print("An unknown exception has occurred")
    return txt