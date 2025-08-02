
import speech_recognition as sr
import pyttsx3
import time
import webbrowser
import musiclibrary
import requests
import google.generativeai as genai

recogniser = sr.Recognizer()
engine = pyttsx3.init('sapi5')  


voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  
engine.setProperty('rate', 170) 

def speak(text):
    print(f"🔊 {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0)  

def aiprocess(command):
    if command.strip() == "":
        speak("I didn't catch that. Please repeat.")
        return

    
    genai.configure(api_key="AIzaSyC_jiNMRMfQTtK00XiNAuxgu_yYuXTNKUw")

    model = genai.GenerativeModel("gemini-1.5-flash")

    chat = model.start_chat(history=[
        {"role": "user", "parts": ["You are Jarvis, a helpful assistant skilled in general tasks."]}
    ])
    response = chat.send_message(command)
    return response.text


def processcommand(c):
    if "open google"  in c:
        webbrowser.open("https://google.com")

    elif "open facebook"  in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube"  in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin"  in c:
        webbrowser.open("https://linkedin.com")

    elif "news" in c:
        api_key = "c48da1eb7e324b61a12f3e75a85d7ee3" 
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"

        try:
            r = requests.get(url)
            data = r.json()

            if data.get("status") == "ok":
                articles = data.get("articles", [])
                speak("📰 Top Headlines (India):")
                for idx, article in enumerate(articles[:5], start=1):
                    speak(f"{idx}. {article.get('title')}")
            else:
                speak(f"Failed to fetch news: {data.get('message')}")
        except Exception as e:
            speak("An error occurred while fetching the news.")
            print(f"Error: {e}")


    elif c.startswith("play"):
        try:
            song = c.replace("play", "").strip().title() 
            if song in musiclibrary.music:
                link = musiclibrary.music[song]
                webbrowser.open(link)
            else:
                speak(f"Sorry, I couldn't find the song '{song}' in your library.")
        except Exception as e:
            speak("Something went wrong while playing the song.")
            print(f"Error: {e}")
    else:
        output=aiprocess(c)
        print(output)
        speak(output)
def listen_command(timeout=5, phrase_time_limit=5):
    with sr.Microphone() as source:
        recogniser.adjust_for_ambient_noise(source)
        speak("listening...")
        print("🎤 Listening...")
        try:
            audio = recogniser.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recogniser.recognize_google(audio, language="en-IN")
            print("✅ You said:", command)
            return command.lower()
        except sr.WaitTimeoutError:
            print("❌ Timeout: No speech detected.")
            
        except sr.UnknownValueError:
            print("❌ Could not understand.")
            
        except sr.RequestError:
            print("❌ Network error.")
            
        return ""


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        
        command = listen_command()

        if not command:
            continue

       

        if "jarvis" in command:
            speak("Yes boss, How can I help you?")
            
            follow_up = listen_command()
            processcommand(follow_up)
            

        if "exit" in command or "quit" in command:
            speak("Goodbye boss.")
            break




