import pyttsx3
from Settings import *

class Audio():
    def __init__(self, settings):
        self.settings = settings
        self.engine = pyttsx3.init()

    def options(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            print("Name:", voice.name)
            print("ID:", voice.id)
            print("Languages:", voice.languages)
            print("Gender:", voice.gender)
            print("Age:", voice.age)
            print("``````````````````````````````````````````")

    def read_page(self, text):
        self.settings = Settings()
        self.engine.setProperty('voice', self.settings.language)
        self.engine.setProperty('rate', self.settings.rate)
        self.engine.setProperty('volume', self.settings.volume)
        self.engine.say(text)
        self.engine.runAndWait()
    
    def set_volume(self, volume):
        self.settings.update('section_audio', 'volume', volume)
        self.engine.setProperty('volume', volume)

    def set_rate(self, rate):
        self.settings.update('section_audio', 'rate', rate)
        self.engine.setProperty('rate', rate)

    def set_language(self, language):
        self.settings.update('section_audio', 'language', language)
        self.engine.setProperty('voice', language)    