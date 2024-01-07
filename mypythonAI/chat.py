# Smit saraiya

import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import datetime

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
        except Exception as e:
            print("me ---> ERROR", str(e))
    
    def wake_up(self, text):
        return True if self.name in text.lower() else False
    
    @staticmethod 
    def action_time():
        return datetime.datetime.now().strftime("%H:%M")        
    
    @staticmethod
    def text_to_speech(text):
        print("AI ---> ", text)
        speaker = gTTS(text=text, lang="en", slow=False)
        speaker.save("response.mp3")
        os.system("afplay response.mp3")
        os.remove("response.mp3")
        
        
        
if  __name__ == "__main__":
    bot = ChatBot(name="computer")
    
    while True:
        bot.speech_to_text()
        # wakeup
        if bot.wake_up(bot.text) is True:
            res = "Hello, my name is computer. What can I do for you?"
        elif "time" in bot.text:
            res = bot.action_time()
        elif any(i in bot.text for i in ["thanks", "thanks"]):
            res = np.random.choice(
                ["You're Welcome!",
                 "Anytime!",
                 "No problem!",
                 "Always here to help!"])
                        
        bot.text_to_speech(res)

