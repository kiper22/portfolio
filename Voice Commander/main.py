# do dodania webscraping, obsługa systemu- pliki monitor, kodowanie/ pisanie
import pyautogui
import pyttsx3
import speech_recognition as sr 
import time
import audio
import screen


continue_mouse_movement = False
r = sr.Recognizer()
engine = pyttsx3.init()

engine.setProperty('rate', 150)
engine.setProperty('voice', 'english')

def recognize_speech():
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=2, phrase_time_limit=8)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio, language="auto")
            print(voice_data)
        except sr.UnknownValueError:
            print("Sorry we didnt expect that!")
        except sr.RequestError:
            print("Sorry, my speech service is down")
        return voice_data

def execute_command(command):
    if "run" in command:
        app_name = command.split("run ")[1]
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.typewrite(app_name)
        time.sleep(1)
        pyautogui.press('enter')
    elif "volume increase" in command:
        audio.volume_increase()
    elif "volume decrease" in command:
        audio.volume_decrease()
    elif "volume mute" in command:
        audio.volume_mute()
    elif "volume unmute" in command:
        audio.volume_unmute()
    elif "set volume" in command:
        audio.set_volume(command)
    elif "screen brightness up" in command:
        screen.screen_brightness_up()
    elif "screen brightness down" in command:
        screen.screen_brightness_down()
    elif "screen brightness set" in command:
        screen.screen_brightness_set(command)
    elif "screen on" in command:
        screen.screen_on()
    elif "screen off" in command:
        screen.screen_off() 
    else:
        print("Command wasnt found")

while True:
    command = recognize_speech()
    execute_command(command)
    
    engine.say("Waiting for next command")
    engine.runAndWait()
