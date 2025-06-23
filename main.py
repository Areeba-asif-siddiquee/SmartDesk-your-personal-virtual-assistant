import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import traceback
from config import groq_api_key
import requests

def say(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")

groq_api_key = "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"

chat_history = [
    {"role": "system", "content": "A helpful voice-based assistant, like Alexa or Siri."}
  ]

if not os.path.exists("AI"):
    os.mkdir("AI")
chat_log_path = os.path.join("AI", "chat_history.txt")

def chat(query):
    try:
        print("You:", query)

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        chat_history.append({"role": "user", "content": query})
        data = {
                "model": "llama3-8b-8192",
                "messages": chat_history
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )

        response.raise_for_status()
        result = response.json()

        reply = result["choices"][0]["message"]["content"].strip()
        chat_history.append({"role": "assistant", "content": reply})

        print("AI:", reply)
        say(reply)

        with open(chat_log_path, "a", encoding="utf-8") as f:
            f.write(f"You: {query}\n AI: {reply}\n\n")

    except Exception as e:
         print("Error in AI response:", e)
         traceback.print_exc()
         say("Sorry, I could not get a response from the AI.")


# Groq API key ==> https://console.groq.com/
def ai(prompt):
    try:
        print("Generating Groq Cloud Response...")

        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": "You are a helpful virtual assistant."},
            {"role": "user", "content": prompt}
        ]

        data = {
            "model": "llama3-8b-8192",
            "messages": messages
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                                 headers=headers,
                                 json=data)

        response.raise_for_status()   #for errors else ignore if o/p is generated
        result = response.json()      #.json()=> returns python dict by default. [result is  a dict

        reply = result["choices"][0]["message"]["content"]
        print("Groq Response:\n", reply)
        say(reply)

        text = f"Groq response for prompt - {prompt}\n *********************\n\n{reply}"

        if not os.path.exists("GroqAI"):
            os.mkdir("GroqAI")

        filename = os.path.join("GroqAI", f"{''.join(prompt.split('intelligence')[1:])}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)
            print(f"Response saved at: {filename}")

    except Exception as e:
        print("Error in Groq API response:", e)
        traceback.print_exc()
        say("Sorry, I could not get a response from Groq.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        print("recogninzing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return "Sorry, I could not understand."

if __name__ == '__main__':
    print('PyCharm')
    say("hello i am smartDesk: your personal virtual assisstance or A.I")

    while True:
        print("listening....")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"],["google" , "https://www.google.com"],["wikipedia","https://www.wikipedia.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"opening {site[0]} ma'am")
                webbrowser.open(site[1])

        if "open music" in query:
            say("opening music ma'am")
            music_path = r"C:\Users\Areeba Siddiquee\Desktop\MAJOR_PROJECT\songs\christmas-romantic-pianonuit-de-noel-271107.mp3"
            os.startfile(music_path)

        if "what is the time" in query:
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"so the time is {strftime}")

        if "using artificial intelligence".lower() in query.lower():
            ai(query)

        if "stop" in query.lower():
           say("Goodbye!")
           break

        else:
            chat(query)

