# Smit saraiya

import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os

class ChatBot():
    def __init__(self, name):
        print("-- starting up", name, "--")
        self.name = name
    
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            audio = recognizer.listen(source)
            # some problem over here
        try:
            self.text = recognizer.recognize_google(audio)
            print("me ---> ", self.text)
        except:
            print("me ---> ERROR")
    
    
    def wake_up(self, text):
        return True if self.name in text.lower() else False
    
    @staticmethod
    def text_to_speech(self, text):
        print("AI ---> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("response.mp3")
        os.system("afplay response.mp3")
        os.remove("response.mp3")
        
        
        
if  __name__ == "__main__":
    bot = ChatBot(name="computer")
    while(True):
        bot.speech_to_text()

