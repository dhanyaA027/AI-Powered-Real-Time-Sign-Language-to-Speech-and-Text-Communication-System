import pyttsx3


class SpeechEngine:

    def __init__(self):
        self.engine = pyttsx3.init()

        # Speech speed
        self.engine.setProperty("rate", 150)

        # Volume
        self.engine.setProperty("volume", 1.0)

        # Try to select an English voice
        voices = self.engine.getProperty("voices")

        if voices:
            for voice in voices:
                voice_name = voice.name.lower()

                if "english" in voice_name or "zira" in voice_name:
                    self.engine.setProperty(
                        "voice",
                        voice.id
                    )
                    break

    def speak(self, text):

        if not text:
            return

        print("Avatar speaking:", text)

        self.engine.say(text)
        self.engine.runAndWait()