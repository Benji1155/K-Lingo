# Import required Libraries
import tkinter as tk
from tkinter import scrolledtext, ttk
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pygame
import io
from gtts import gTTS
from PIL import Image, ImageTk
import re
import nltk

# Defining main class/program
class SpeechRecognitionApp:
    
    # Defining a function that takes in the Window GUI and self GUI
    def __init__(self, Window):
        
        # Defining main window parameters
        self.Window = Window
        self.Window.title("K-Lingo") # Title the window
        self.Window.geometry("460x550") # Set window size
        
        # Making the window fixed size so it cannot be changed by user
        self.Window.resizable(width=False, height=False)

        # Initializing the speech recognition as recognizer in self
        self.recognizer = sr.Recognizer()

        # Loading logo image with Pillow and resizing
        try:
            image = Image.open("images/logo.png") # Directory of image is fixed
            image = image.resize((int(image.width * 0.7), int(image.height * 0.7)))  # Resizing the image to fit application better
            self.logo_image = ImageTk.PhotoImage(image) # Loading image
        except FileNotFoundError:
            # If error occurs end more nicely
            self.logo_image = None 

        # Making all the styling
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#dabfff') # Frame style
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), background='#907ad6', foreground='#4f518c', padding=10) # Button style
        self.style.configure('TLabel', font=('Helvetica', 12, 'bold'), background='#dabfff', foreground='#4f518c') # Label style
        self.style.configure('TText', font=('Helvetica', 10), background='#ffffff', foreground='#000000') # Text style

        # Making the frame
        self.frame = ttk.Frame(Window, padding="10", style='TFrame')
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Making the logo label
        if self.logo_image:
            self.logo_label = tk.Label(self.frame, image=self.logo_image, background='#dabfff')
            self.logo_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Setting the text output area
        self.text_area_label = ttk.Label(self.frame, text="Output:", style='TLabel')
        self.text_area_label.grid(row=1, column=0, columnspan=2, sticky=tk.W)

        self.text_area = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=60, height=15, font=("Helvetica", 10), bg='#ffffff', fg='#000000')
        self.text_area.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        self.text_area.config(state=tk.DISABLED)

        # The buttons config
        self.start_button = ttk.Button(self.frame, text="Start Translating", command=self.start_listening, style='TButton')
        self.start_button.grid(row=3, column=0, padx=10, pady=1, sticky=tk.W)

        self.stop_button = ttk.Button(self.frame, text="Stop Translating", command=self.stop_listening, state=tk.DISABLED, style='TButton')
        self.stop_button.grid(row=3, column=1, padx=10, pady=1, sticky=tk.E)

        self.clear_button = ttk.Button(self.frame, text="Clear", command=self.clear_text_area, style='TButton')
        self.clear_button.grid(row=4, column=0, padx=10, pady=0, sticky=tk.W)

        self.exit_button = ttk.Button(self.frame, text="Exit", command=self.Window.quit, style='TButton')
        self.exit_button.grid(row=4, column=1, padx=10, pady=0, sticky=tk.E)

        self.stop_listening_func = None

        # Initializing pygame mixer for audio playback
        pygame.mixer.init()
    
    # Function to try call the translation
    def callback(self, recognizer, audio):
        
        # Try getting a translation and recognized sentence
        try:
            # Use the recognizer with the audio input and save it as text
            text = recognizer.recognize_google(audio)

            # Send the recognized sentence to chat window in English
            self.append_text(f"You said: {text}\n")

            # Attempt to get a translation and save it
            translated_text = self.translate_to_korean(text)
            
            # if translation successful send translation to output window and say the Korean
            # if not, give back an error message
            if translated_text:
                self.append_text(f"Translated: {translated_text}\n")
                self.speak(translated_text)
            else:
                self.append_text("Translation failed\n")
        
        # Error catching and error messages delivered
        except sr.UnknownValueError:
            self.append_text("Could not understand audio\n")
        except sr.RequestError as e:
            self.append_text(f"Could not request results; {e}\n")
        except Exception as e:
            self.append_text(f"Error: {e}\n")
    
    # Translation function, takes in self and the text
    def translate_to_korean(self, text):
        # Try translate the text or return an error
        try:
            
            # Google translate to translate to Korean characters 
            translated_text = GoogleTranslator(source='auto', target='ko').translate(text)
            
            # Return the text
            return translated_text
        except Exception as e:
            
            # Error message
            self.append_text(f"Translation error: {e}\n")
            return None
    
    # Speak function to say the translation
    def speak(self, text):
        try:
            # Creating a gTTS object and convert text to speech
            tts = gTTS(text=text, lang='ko') # setting the language to Korean and input text as text
            speech_bytes = io.BytesIO()
            tts.write_to_fp(speech_bytes)
            speech_bytes.seek(0)

            # Loading the speech bytes into mixer and play
            pygame.mixer.music.load(speech_bytes)
            pygame.mixer.music.play()

            # Waiting until the speech finishes playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        # Give an error message if it fails
        except Exception as e:
            self.append_text(f"TTS error: {e}\n")
    
    # Function for start listening button
    def start_listening(self):
        
        # Tell user it is listening in output 
        self.append_text("Listening...\n")
        self.start_button.config(state=tk.DISABLED) # Disable button
        self.stop_button.config(state=tk.NORMAL)
        
        # Setting up microphone
        mic = sr.Microphone()
        
        # Setting mic as the source with ambient noise reduction to get better results
        with mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
        # Setting the listening in background to be stopped when button pressed "stop listening"
        self.stop_listening_func = self.recognizer.listen_in_background(mic, self.callback)
    
    # Function to stop listening to input mic
    def stop_listening(self):
        
        # Stops the listening and sets button to disabled
        if self.stop_listening_func:
            self.stop_listening_func(wait_for_stop=False)
            self.append_text("Stopped listening.\n")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    # Clears the output window
    def clear_text_area(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
    
    # Sends a message to the output window
    def append_text(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)

# Main where the program starts
if __name__ == "__main__":
    Window = tk.Tk()
    app = SpeechRecognitionApp(Window)
    Window.mainloop()
