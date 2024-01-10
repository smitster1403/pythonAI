# Smit saraiya
# my first AI ChatBot

import time
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import os
import datetime
import transformers

class ChatBot():
    def __init__(self, name):
        print("-- starting up", name, "--")
        self.name = name
    
    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            audio = recognizer.listen(source)
            self.text = "ERROR"
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
        statbuf = os.stat("response.mp3")
        mbytes = statbuf.st_size / 1024
        duration = mbytes / 2000
        os.system("afplay response.mp3")
        time.sleep(int(50*duration))
        os.remove("response.mp3")
        
        
        
if  __name__ == "__main__":
    bot = ChatBot(name="computer")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True
    while ex:
        bot.speech_to_text()
        # wakeup
        if bot.wake_up(bot.text) is True:
            res = "Hello, my name is computer. What can I do for you?"
        elif "time" in bot.text:
            res = "The time is " + str(bot.action_time())
        elif any(i in bot.text for i in ["thank", "thanks"]):
            res = np.random.choice(
                ["You're Welcome!",
                 "Anytime!",
                 "No problem!",
                 "Always here to help!"])
        elif any(i in bot.text for i in ["exit", "close", "bye"]):
            res = np.random.choice(
                ["See you soon!",
                 "Bye!",
                 "Goodbye!",
                 "Ciao!"])
            ex = False
        else:
            if bot.text == "ERROR":
                res = "Sorry, I didn't get that."
            else:
                chat = nlp(transformers.Conversation(bot.text), pad_token_id=50256)
                res = str(chat)
                res = res[res.find("bot >> ")+6:].strip()
        bot.text_to_speech(res)
        
    print("-- shutting down --")
