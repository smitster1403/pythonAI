# Smit saraiya
# my first AI ChatBot
from urllib.error import URLError
import time
import requests
import numpy as np
import speech_recognition as sr
from googlesearch import search
from gtts import gTTS
from lxml import html
import os, string
import datetime
import transformers
import playsound as ps
from bs4 import BeautifulSoup
import pygame
import certifi

print(certifi.where())
os.environ['SSL_CERT_FILE'] = certifi.where()
import tensorflow as tf
try:
    from googlesearch import search
except ImportError:
    print("Module 'google' does not exist")


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
        return True if self.name.lower() in text.lower() else False
    
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
        
        
# -- MAIN --
if  __name__ == "__main__":
    bot = ChatBot(name="Iris")
    nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    ex = True
    fallback = ["Sorry, I didn't get that.", "Sorry, come again?", "Maybe you spoke gibberish. Please repeat yourself."]
    # Startup sound
    pygame.mixer.init()
    pygame.mixer.music.load("/Users/smitster1403/Desktop/pythonprojects/pythonAI/mypythonAI/start.mp3")
    pygame.mixer.music.play()
    while ex:
        bot.speech_to_text()
        # wakeup
        if bot.wake_up(bot.text) is True:
            res = "Hello, my name is Iris. What can I do for you?"
        elif "time" in bot.text:
            res = "The time is " + str(bot.action_time())
        elif any(i in bot.text for i in ["thank", "thanks"]):
            # Responses to being thanked.
            res = np.random.choice(
                ["You're Welcome!",
                 "Anytime!",
                 "No problem!",
                 "Always here to help!"]) + np.random.choice([
                     " Anything else you need me to do?",
                     " What else can I assist you with?",
                     " You ask and I deliver!"
                 ])
        elif any(i in bot.text for i in ["exit", "close", "bye", "goodbye"]):
            # Salutations - leaving
            res = np.random.choice(
                ["See you soon!",
                 "Bye!",
                 "Goodbye!",
                 "Ciao!"])
            ex = False
            pygame.mixer.music.play()
        elif "search for" in bot.text:
            query = bot.text.split("search for ", 1)[1]
            res = np.random.choice(["\nHere are the responses I got from google...", "\nSure, here is what I found on google...", "\nThis is what Google returns for"+query])
            for attempt in range(5):
                try:
                    for j in search(query, tld="com",num=10, stop = 10, pause=4):
                        print(j)
                    break
                except URLError:
                    print("Connection reset by peer, retrying...")
                
        else:
            # fallback text to say when input speech is not understood.
            res = np.random.choice(fallback)
        bot.text_to_speech(res)
        
    print("-- shutting down --")
