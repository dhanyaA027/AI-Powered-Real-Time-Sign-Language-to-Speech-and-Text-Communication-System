import pyttsx3


class TextToSpeech:

    def __init__(self):

        print("Initializing Text-to-Speech...")

        self.engine = pyttsx3.init()

        # ----------------------------------------------------
        # Speech rate
        # ----------------------------------------------------

        self.engine.setProperty(
            "rate",
            150
        )

        # ----------------------------------------------------
        # Volume
        # ----------------------------------------------------

        self.engine.setProperty(
            "volume",
            1.0
        )

        print("Text-to-Speech ready.")

    # ========================================================
    # SPEAK
    # ========================================================

    def speak(self, text):

        if text is None:
            return

        text = str(text).strip()

        if text == "":
            return

        print()
        print("TTS SPEAKING:")
        print(text)

        self.engine.say(text)

        self.engine.runAndWait()

    # ========================================================
    # STOP
    # ========================================================

    def stop(self):

        self.engine.stop()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("Testing Text-to-Speech...")

    tts = TextToSpeech()

    tts.speak(
        "Hello. Welcome to Vidhya Shree sign language system."
    )

    print("TTS test completed.")