import speech_recognition as sr


class VoiceRecognizer:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone()

    # ========================================================
    # LISTEN
    # ========================================================

    def listen(self):

        print()
        print("=" * 55)
        print("Listening...")
        print("=" * 55)

        try:

            with self.microphone as source:

                print("Adjusting microphone...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                print("Speak now...")

                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=10
                )

            print("Recognizing speech...")

            text = self.recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            text = text.upper().strip()

            print()
            print("Recognized:")
            print(text)
            print()

            return text

        except sr.WaitTimeoutError:

            print(
                "No speech detected."
            )

            return ""

        except sr.UnknownValueError:

            print(
                "Sorry, I could not understand the speech."
            )

            return ""

        except sr.RequestError as error:

            print(
                "Speech recognition service error:"
            )

            print(error)

            return ""

        except Exception as error:

            print(
                "Voice error:"
            )

            print(error)

            return ""


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("VIDHYA SHREE VOICE RECOGNITION TEST")
    print("=" * 55)

    recognizer = VoiceRecognizer()

    while True:

        result = recognizer.listen()

        if result:

            print(
                "FINAL RESULT:",
                result
            )

        choice = input(
            "\nPress ENTER to listen again "
            "or type Q to quit: "
        )

        if choice.upper() == "Q":

            break

    print(
        "Voice test finished."
    )