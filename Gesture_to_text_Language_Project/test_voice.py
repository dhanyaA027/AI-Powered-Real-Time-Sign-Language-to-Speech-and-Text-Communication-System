import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

engine.say("Hello. I am the your AI avatar.")
engine.runAndWait()