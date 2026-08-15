import sys
import os
import threading
import tkinter as tk


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.dirname(__file__))


# ============================================================
# IMPORTS
# ============================================================

from avatar.avatar import SignLanguageAvatar
from voice import VoiceRecognizer


# ============================================================
# APPLICATION
# ============================================================

class VidhyaShreeApp:

    def __init__(self):

        print("=" * 60)
        print("VIDHYA SHREE APPLICATION")
        print("=" * 60)

        # ----------------------------------------------------
        # Create avatar
        # ----------------------------------------------------

        self.avatar = SignLanguageAvatar()

        # ----------------------------------------------------
        # Create voice recognizer
        # ----------------------------------------------------

        self.voice = VoiceRecognizer()

        self.is_listening = False

        # ----------------------------------------------------
        # Create control panel
        # ----------------------------------------------------

        self.create_control_panel()


    # ========================================================
    # CONTROL PANEL
    # ========================================================

    def create_control_panel(self):

        root = self.avatar.root

        # Make sure window is large enough
        root.geometry("1100x850")

        # ----------------------------------------------------
        # Frame
        # ----------------------------------------------------

        frame = tk.Frame(
            root,
            bg="white",
            bd=3,
            relief="ridge"
        )

        frame.place(
            x=300,
            y=650,
            width=500,
            height=170
        )

        # ----------------------------------------------------
        # Heading
        # ----------------------------------------------------

        heading = tk.Label(
            frame,
            text="VOICE CONTROL",
            font=("Arial", 16, "bold"),
            bg="white"
        )

        heading.pack(
            pady=8
        )

        # ----------------------------------------------------
        # BUTTON
        # ----------------------------------------------------

        self.listen_button = tk.Button(
            frame,
            text="START LISTENING",
            font=("Arial", 16, "bold"),
            command=self.button_clicked,
            bg="green",
            fg="white",
            width=22,
            height=2
        )

        self.listen_button.pack(
            pady=5
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        self.status = tk.Label(
            frame,
            text="Click the button and speak",
            font=("Arial", 11),
            bg="white"
        )

        self.status.pack()


    # ========================================================
    # BUTTON CLICKED
    # ========================================================

    def button_clicked(self):

        print()
        print("=" * 60)
        print("BUTTON CLICKED!")
        print("=" * 60)

        if self.is_listening:

            print("Already listening.")

            return

        self.is_listening = True

        self.listen_button.config(
            text="LISTENING...",
            bg="red",
            state=tk.DISABLED
        )

        self.status.config(
            text="Listening... SPEAK NOW"
        )

        # ----------------------------------------------------
        # Start microphone thread
        # ----------------------------------------------------

        thread = threading.Thread(
            target=self.listen,
            daemon=True
        )

        thread.start()


    # ========================================================
    # LISTEN
    # ========================================================

    def listen(self):

        print()
        print("MICROPHONE THREAD STARTED")
        print()

        try:

            sentence = self.voice.listen()

            print()
            print("=" * 60)
            print("VOICE RETURNED")
            print(repr(sentence))
            print("=" * 60)

            # ------------------------------------------------
            # Send result back to Tkinter
            # ------------------------------------------------

            self.avatar.root.after(
                0,
                lambda: self.handle_sentence(sentence)
            )

        except Exception as error:

            print()
            print("=" * 60)
            print("VOICE ERROR")
            print(error)
            print("=" * 60)

            self.avatar.root.after(
                0,
                lambda: self.handle_error(error)
            )


    # ========================================================
    # HANDLE SENTENCE
    # ========================================================

    def handle_sentence(
        self,
        sentence
    ):

        self.is_listening = False

        self.listen_button.config(
            text="START LISTENING",
            bg="green",
            state=tk.NORMAL
        )

        # ----------------------------------------------------
        # Nothing recognized
        # ----------------------------------------------------

        if not sentence:

            self.status.config(
                text="Nothing recognized"
            )

            return

        # ----------------------------------------------------
        # Convert to uppercase
        # ----------------------------------------------------

        sentence = sentence.upper().strip()

        print()
        print("=" * 60)
        print("FINAL SENTENCE")
        print(sentence)
        print("=" * 60)

        self.status.config(
            text=sentence
        )

        # ----------------------------------------------------
        # SEND SENTENCE TO AVATAR
        # ----------------------------------------------------

        try:

            self.avatar.show_sentence(
                sentence
            )

        except Exception as error:

            print()
            print("AVATAR ERROR:")
            print(error)

            self.status.config(
                text="Avatar error"


            )


    # ========================================================
    # ERROR
    # ========================================================

    def handle_error(
        self,
        error
    ):

        self.is_listening = False

        self.listen_button.config(
            text="START LISTENING",
            bg="green",
            state=tk.NORMAL
        )

        self.status.config(
            text="Voice error"
        )


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.avatar.root.mainloop()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app = VidhyaShreeApp()

    app.run()