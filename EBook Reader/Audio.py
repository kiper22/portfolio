import pyttsx3
from Settings import *


class Audio():
    def __init__(self, master, settings):
        self.settings = settings
        self.master = master
        self.playing = False
        # self.read_page(self.settings.text)
    
    def __del__(self):
        print('destroyed')

    def read_page(self, text):
        # better add dict =='Polski': pl== etc and check by 'pl' in variable.split('\')[-1]
        # and connect this voices to settings
        self.engine = pyttsx3.init()
        
        
        self.voices = self.engine.getProperty('voices')
        if self.settings.language == 'Polski':
            self.engine.setProperty('voice', self.voices[0].id)
        elif self.settings.language == 'English':
            self.engine.setProperty('voice', self.voices[1].id)
        
        self.engine.setProperty('rate', self.settings.rate)
        self.engine.setProperty('volume', self.settings.volume)
        
        self.engine.say(text)
        self.engine.runAndWait()
    
    def stop_audio(self):
        self.playing = False
        self.engine.stop()
        self.engine.endLoop()
