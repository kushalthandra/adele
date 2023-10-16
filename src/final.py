import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
import openai

# Set your OpenAI API key
openai.api_key = 'Your API key'

# Initialize the Tkinter app
root = tk.Tk()
root.title("Adele Assistant")

# Set the dimensions of the window and center it on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Add a background image
background_image = tk.PhotoImage(file="images/bg.gif")  # Replace with your image file
background_label = tk.Label(root, image=background_image)#it is used to create a user interface with a background gif
background_label.place(relwidth=1, relheight=1)

# Initialize the speech recognition engine
recog = sr.Recognizer() #this variable is used store and record the audio input from the user

# Initialize the text-to-speech engine
engine = pyttsx3.init() #it is used to configure the tts engine

# Variables to control recording and prompt generation
recording = False
generation = False
txt = ""
response_text = ""

# Function to handle audio recording and prompt generation
def record_and_generate():
    global recording, generation, txt, response_text
    while recording:
        with sr.Microphone() as source:
            print("Speak Anything:")
            recog.adjust_for_ambient_noise(source) #this line of code is optional and can be removed if working in an isolated noise-free environment
            try:
                audio = recog.listen(source)
                print("Audio recording completed")
                txt = recog.recognize_google(audio) #this variable stores the transcription of the input audio by the end user
                print(f"Transcription: {txt}")
                if generation:
                    response = generate_response(txt) #this is used to send the transcription as a prompt to the chat gpt
                    response_text = response #to configure and read the response this variable is used 
                    speak_text(response) #this function is called to convert the generated response into audio and generate output
            except Exception as e:
                print("An unknown exception has occurred")

# Function to start or stop audio recording and prompt generation
def toggle_recording_generation():
    global recording, generation #the recording and generation are flag variables when they are true the respective action occurs
    if not recording:
        recording = True
        generation = True
        threading.Thread(target=record_and_generate).start()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
    else:
        recording = False
        generation = False
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

# Function to generate a response using OpenAI
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003", #there are different types of engines to configure here we have used davinci 003 powered by gpt 3 you can read through the chatgpt api docs to know more about different ypes of engines
        prompt=prompt,
        max_tokens=100,#set number of tokens to generate this variable can be maxed until the limit of 5000 tokens anything more than that may result in system crash
        n=1,
        stop=None,
        temperature=0.5,#this value must lie in the range of 0 to 1 only anything more than that will result in system errors
    )
    return response["choices"][0]["text"] #the generated response is returned 

# Function to speak text using the text-to-speech engine
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Create buttons
start_button = tk.Button(root, text="Start Recording", command=toggle_recording_generation)
stop_button = tk.Button(root, text="Stop Recording", command=toggle_recording_generation)
stop_button.config(state=tk.DISABLED)

# Layout
start_button.pack(side=tk.BOTTOM, pady=10)  # Place the "Start Recording" button at the bottom center with some padding
stop_button.pack(side=tk.BOTTOM)  # Place the "Stop Recording" button just below the "Start Recording" button

# Create labels to display the value of the txt and response_text variables
txt_label = tk.Label(root, text="", bg="white")
txt_label.pack(side=tk.TOP, pady=20)  # Place at the bottom

# Create a Frame for the "Response" heading and the response text
response_frame = tk.Frame(root)
response_frame.pack(side=tk.TOP, pady=10)  # Place at the bottom

response_label = tk.Label(response_frame, text="Response: ", bg="white")
response_label.pack(side=tk.LEFT)  # Place the "Response" heading to the left within the frame

response_text_label = tk.Label(response_frame, text="", bg="white")
response_text_label.pack(side=tk.LEFT)  # Place the response text to the left within the frame

# Center the "Response" heading
response_label.pack_configure(anchor="center")

# Function to update the txt_label and response_text_label text
def update_labels():
    global txt, response_text
    txt_label.config(text=f"Transcription: {txt}")
    response_text_label.config(text=response_text)
    root.after(1000, update_labels)  # Update every second

update_labels()

# Run the Tkinter main loop
root.mainloop()
