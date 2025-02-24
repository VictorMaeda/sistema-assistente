import speech_recognition as sr
from gtts import gTTS
import playsound
import pyjokes
import wikipedia
import winshell
from pygame import mixer
import pyaudio
from datetime import datetime
import webbrowser
import os
import requests

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available")
    return said.lower()

#speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

#function to respond to commands
def respond(text):
    print("Text from get audio " + text)
    if 'youtube' in text:
        speak("What do you want to search for?")
        keyword = get_audio()
        if keyword!= '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            speak(f"Here is what I have found for {keyword} on youtube")
    elif 'search' in text:
        speak("What do you want to search for?")
        query = get_audio()
        if query !='':
            result = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia")
            print(result)
            speak(result)
    elif 'joke' in text:
        speak(pyjokes.get_joke())
    elif 'empty recycle bin' in text:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Recycle bin emptied")
    elif 'dollar' in text:
        response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
        data = response.json()
        result = "Um dólar está " + str(float(data["USDBRL"]["bid"])) + " reais"
        print(result)
        speak(result)
    elif 'what time' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        speak(strTime)
    elif 'exit' in text:
        speak("Goodbye, till next time")
        exit()
while True:
    print("I am listening...")
    text = get_audio()
    respond(text)