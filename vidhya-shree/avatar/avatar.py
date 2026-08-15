import tkinter as tk
import threading
import time

# ------------------------------------------------------------
# Optional libraries
# ------------------------------------------------------------

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False


# ============================================================
# BEAUTIFUL FEMALE AI ROBOT AVATAR
# ============================================================

class SignLanguageAvatar:

    def __init__(self):

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root = tk.Tk()

        self.root.title(
            "AI Sign Language Female Robot - Vidhya Shree"
        )

        self.root.geometry("1250x780")
        self.root.minsize(1100, 700)

        self.root.configure(
            bg="#eef3f8"
        )

        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            self.root,
            width=1250,
            height=780,
            bg="#eef3f8",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.mouth_running = False
        self.current_sentence = ""

        self.left_hand_angle = 0
        self.right_hand_angle = 0

        self.voice_running = False
        self.speaking = False

        self.hand_animation_id = None
        self.mouth_animation_id = None

        # ----------------------------------------------------
        # SENTENCES
        # ----------------------------------------------------

        self.sentences = {

            "HI HOW ARE YOU":
                "HI HOW ARE YOU",

            "MY NAME IS AVATAR":
                "MY NAME IS AVATAR",

            "NICE TO MEET YOU":
                "NICE TO MEET YOU",

            "HOW CAN I HELP YOU":
                "HOW CAN I HELP YOU",

            "HAVE A NICE DAY":
                "HAVE A NICE DAY"
        }

        # ----------------------------------------------------
        # DRAW EVERYTHING
        # ----------------------------------------------------

        self.draw_background()

        self.draw_robot()

        self.create_control_panel()

        self.create_sentence_buttons()

        # ----------------------------------------------------
        # INITIAL STATUS
        # ----------------------------------------------------

        self.set_status(
            "Ready - choose a sentence or use Voice Control"
        )

    # ========================================================
    # BACKGROUND
    # ========================================================

    def draw_background(self):

        self.canvas.create_rectangle(
            0,
            0,
            1250,
            780,
            fill="#eef3f8",
            outline=""
        )

        # Header
        self.canvas.create_text(
            625,
            30,
            text="AI FEMALE SIGN LANGUAGE ROBOT",
            font=("Arial", 25, "bold"),
            fill="#263b59"
        )

        self.canvas.create_text(
            625,
            62,
            text="Vidhya Shree - Speech • Lip Sync • Hand Animation",
            font=("Arial", 13),
            fill="#607d9a"
        )

        # Floor
        self.canvas.create_oval(
            170,
            690,
            760,
            745,
            fill="#dce5ee",
            outline=""
        )

    # ========================================================
    # ROBOT
    # ========================================================

    def draw_robot(self):

        # ----------------------------------------------------
        # Robot center
        # ----------------------------------------------------

        cx = 465

        # ----------------------------------------------------
        # NECK
        # ----------------------------------------------------

        self.canvas.create_rectangle(
            430,
            265,
            500,
            315,
            fill="#cfd9e3",
            outline="#7b8c9c",
            width=2
        )

        self.canvas.create_oval(
            445,
            275,
            485,
            300,
            fill="#5dd6d1",
            outline="#388f91",
            width=2
        )

        # ----------------------------------------------------
        # BODY
        # ----------------------------------------------------

        self.canvas.create_oval(
            330,
            300,
            600,
            650,
            fill="#dce5ed",
            outline="#718394",
            width=3
        )

        # Chest plate
        self.canvas.create_oval(
            385,
            330,
            545,
            545,
            fill="#f5f8fb",
            outline="#9aaab8",
            width=2
        )

        # Chest center
        self.canvas.create_oval(
            448,
            390,
            482,
            424,
            fill="#55d6d1",
            outline="#287f82",
            width=2
        )

        self.canvas.create_oval(
            458,
            400,
            472,
            414,
            fill="#ffffff",
            outline=""
        )

        # ----------------------------------------------------
        # WAIST
        # ----------------------------------------------------

        self.canvas.create_oval(
            370,
            545,
            560,
            610,
            fill="#252f3b",
            outline="#151d25",
            width=2
        )

        # ----------------------------------------------------
        # HEAD
        # ----------------------------------------------------

        self.canvas.create_oval(
            310,
            90,
            610,
            335,
            fill="#e9eef3",
            outline="#687887",
            width=3
        )

        # Face plate
        self.canvas.create_oval(
            330,
            115,
            590,
            315,
            fill="#f6f8fa",
            outline="#c1ccd6",
            width=2
        )

        # ----------------------------------------------------
        # HAIR
        # ----------------------------------------------------

        self.canvas.create_oval(
            315,
            75,
            610,
            210,
            fill="#202a38",
            outline="#18202b",
            width=2
        )

        # Side hair
        self.canvas.create_oval(
            315,
            130,
            365,
            270,
            fill="#202a38",
            outline=""
        )

        self.canvas.create_oval(
            560,
            130,
            610,
            270,
            fill="#202a38",
            outline=""
        )

        # Hair highlight
        self.canvas.create_arc(
            335,
            85,
            550,
            180,
            start=180,
            extent=150,
            style=tk.ARC,
            outline="#53647a",
            width=5
        )

        # ----------------------------------------------------
        # EARS
        # ----------------------------------------------------

        self.canvas.create_oval(
            298,
            190,
            330,
            235,
            fill="#cfd9e3",
            outline="#718394",
            width=2
        )

        self.canvas.create_oval(
            590,
            190,
            622,
            235,
            fill="#cfd9e3",
            outline="#718394",
            width=2
        )

        # ----------------------------------------------------
        # EYES
        # ----------------------------------------------------

        # Left eye
        self.canvas.create_oval(
            375,
            165,
            425,
            215,
            fill="#1c2634",
            outline="#0d141d",
            width=2
        )

        # Right eye
        self.canvas.create_oval(
            495,
            165,
            545,
            215,
            fill="#1c2634",
            outline="#0d141d",
            width=2
        )

        # Eye glow
        self.left_eye_glow = self.canvas.create_oval(
            390,
            176,
            404,
            190,
            fill="#ffffff",
            outline=""
        )

        self.right_eye_glow = self.canvas.create_oval(
            510,
            176,
            524,
            190,
            fill="#ffffff",
            outline=""
        )

        # ----------------------------------------------------
        # EYEBROWS
        # ----------------------------------------------------

        self.canvas.create_line(
            370,
            150,
            425,
            142,
            fill="#354352",
            width=5,
            smooth=True
        )

        self.canvas.create_line(
            495,
            142,
            550,
            150,
            fill="#354352",
            width=5,
            smooth=True
        )

        # ----------------------------------------------------
        # NOSE
        # ----------------------------------------------------

        self.canvas.create_line(
            460,
            205,
            450,
            238,
            465,
            243,
            fill="#8796a4",
            width=3,
            smooth=True
        )

        # ----------------------------------------------------
        # MOUTH AREA
        # ----------------------------------------------------

        self.canvas.create_oval(
            415,
            245,
            505,
            285,
            fill="#eef2f5",
            outline="#a3b0bc",
            width=2
        )

        # Actual mouth
        self.mouth = self.canvas.create_oval(
            438,
            254,
            482,
            270,
            fill="#7c3f54",
            outline="#4b2633",
            width=2
        )

        # Smile
        self.mouth_smile = self.canvas.create_arc(
            420,
            238,
            500,
            285,
            start=200,
            extent=140,
            style=tk.ARC,
            outline="#596b7b",
            width=3
        )

        # ----------------------------------------------------
        # SHOULDERS
        # ----------------------------------------------------

        self.canvas.create_oval(
            280,
            315,
            390,
            405,
            fill="#d3dde6",
            outline="#718394",
            width=3
        )

        self.canvas.create_oval(
            540,
            315,
            650,
            405,
            fill="#d3dde6",
            outline="#718394",
            width=3
        )

        # ----------------------------------------------------
        # ARMS
        # ----------------------------------------------------

        self.left_upper_arm = self.canvas.create_line(
            330,
            350,
            265,
            450,
            fill="#d5dfe8",
            width=45,
            capstyle=tk.ROUND
        )

        self.right_upper_arm = self.canvas.create_line(
            600,
            350,
            665,
            450,
            fill="#d5dfe8",
            width=45,
            capstyle=tk.ROUND
        )

        # Elbows
        self.canvas.create_oval(
            245,
            425,
            285,
            465,
            fill="#bcc9d4",
            outline="#718394",
            width=2
        )

        self.canvas.create_oval(
            645,
            425,
            685,
            465,
            fill="#bcc9d4",
            outline="#718394",
            width=2
        )

        # Forearms
        self.left_forearm = self.canvas.create_line(
            265,
            450,
            250,
            535,
            fill="#e0e7ed",
            width=38,
            capstyle=tk.ROUND
        )

        self.right_forearm = self.canvas.create_line(
            665,
            450,
            680,
            535,
            fill="#e0e7ed",
            width=38,
            capstyle=tk.ROUND
        )

        # ----------------------------------------------------
        # ROBOT HANDS
        # ----------------------------------------------------

        self.left_hand_parts = []
        self.right_hand_parts = []

        self.draw_robot_hand(
            250,
            555,
            self.left_hand_parts,
            mirror=True
        )

        self.draw_robot_hand(
            680,
            555,
            self.right_hand_parts,
            mirror=False
        )

        # ----------------------------------------------------
        # LEGS
        # ----------------------------------------------------

        self.canvas.create_line(
            420,
            590,
            390,
            680,
            fill="#dce5ed",
            width=55,
            capstyle=tk.ROUND
        )

        self.canvas.create_line(
            510,
            590,
            540,
            680,
            fill="#dce5ed",
            width=55,
            capstyle=tk.ROUND
        )

        # Knees
        self.canvas.create_oval(
            365,
            650,
            415,
            700,
            fill="#becbd6",
            outline="#718394",
            width=2
        )

        self.canvas.create_oval(
            515,
            650,
            565,
            700,
            fill="#becbd6",
            outline="#718394",
            width=2
        )

        # Feet
        self.canvas.create_oval(
            350,
            685,
            430,
            720,
            fill="#dce5ed",
            outline="#718394",
            width=3
        )

        self.canvas.create_oval(
            525,
            685,
            605,
            720,
            fill="#dce5ed",
            outline="#718394",
            width=3
        )

    # ========================================================
    # ROBOT HAND
    # ========================================================

    def draw_robot_hand(
        self,
        x,
        y,
        parts,
        mirror=False
    ):

        direction = -1 if mirror else 1

        # Palm
        palm = self.canvas.create_oval(
            x - 35,
            y - 30,
            x + 35,
            y + 35,
            fill="#dce5ed",
            outline="#718394",
            width=2
        )

        parts.append(palm)

        # Fingers
        finger_positions = [-25, -8, 9, 26]

        for index, offset in enumerate(finger_positions):

            length = 48

            if index == 0:
                length = 45

            elif index == 3:
                length = 38

            fx = x + offset

            end_y = y - length

            finger = self.canvas.create_line(
                fx,
                y - 5,
                fx + direction * 3,
                end_y,
                fill="#dce5ed",
                width=13,
                capstyle=tk.ROUND
            )

            parts.append(finger)

            # Finger joint
            joint = self.canvas.create_oval(
                fx - 7,
                end_y - 7,
                fx + 7,
                end_y + 7,
                fill="#bcc9d4",
                outline="#718394",
                width=1
            )

            parts.append(joint)

        # Thumb
        thumb = self.canvas.create_line(
            x + direction * 25,
            y + 10,
            x + direction * 48,
            y - 5,
            fill="#dce5ed",
            width=15,
            capstyle=tk.ROUND
        )

        parts.append(thumb)

    # ========================================================
    # CONTROL PANEL
    # ========================================================

    def create_control_panel(self):

        # Panel is to the RIGHT of the robot's head
        # and above the hand.

        self.canvas.create_rectangle(
            720,
            105,
            1185,
            385,
            fill="#ffffff",
            outline="#c7d3df",
            width=2
        )

        self.canvas.create_text(
            952,
            130,
            text="VOICE CONTROL",
            font=("Arial", 20, "bold"),
            fill="#263b59"
        )

        self.canvas.create_text(
            952,
            158,
            text="Speak or type a sentence",
            font=("Arial", 12),
            fill="#718394"
        )

        # ----------------------------------------------------
        # Entry
        # ----------------------------------------------------

        self.sentence_entry = tk.Entry(
            self.root,
            font=("Arial", 13),
            width=38,
            relief=tk.FLAT,
            bg="#f1f5f8"
        )

        self.sentence_entry.place(
            x=745,
            y=180,
            width=415,
            height=38
        )

        self.sentence_entry.insert(
            0,
            "HI HOW ARE YOU"
        )

        # ----------------------------------------------------
        # SPEAK BUTTON
        # ----------------------------------------------------

        self.speak_button = tk.Button(
            self.root,
            text="🔊  SPEAK",
            font=("Arial", 12, "bold"),
            bg="#55c7c2",
            fg="white",
            activebackground="#3ca8a4",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.speak_from_entry
        )

        self.speak_button.place(
            x=745,
            y=230,
            width=195,
            height=45
        )

        # ----------------------------------------------------
        # VOICE BUTTON
        # ----------------------------------------------------

        self.listen_button = tk.Button(
            self.root,
            text="🎤  START LISTENING",
            font=("Arial", 12, "bold"),
            bg="#557fc7",
            fg="white",
            activebackground="#3f67a8",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_voice_control
        )

        self.listen_button.place(
            x=965,
            y=230,
            width=195,
            height=45
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 11),
            bg="#ffffff",
            fg="#607d9a"
        )

        self.status_label.place(
            x=745,
            y=290,
            width=415,
            height=30
        )

        # ----------------------------------------------------
        # CURRENT SENTENCE
        # ----------------------------------------------------

        self.current_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#263b59",
            wraplength=400
        )

        self.current_label.place(
            x=745,
            y=325,
            width=415,
            height=45
        )

    # ========================================================
    # SENTENCE BUTTONS
    # ========================================================

    def create_sentence_buttons(self):

        self.canvas.create_text(
            925,
            425,
            text="QUICK SENTENCES",
            font=("Arial", 18, "bold"),
            fill="#263b59"
        )

        sentences = list(self.sentences.keys())

        x = 735
        y = 460

        for sentence in sentences:

            button = tk.Button(
                self.root,
                text=sentence,
                font=("Arial", 10, "bold"),
                bg="#ffffff",
                fg="#3c536b",
                activebackground="#dceff0",
                relief=tk.RIDGE,
                cursor="hand2",
                command=lambda s=sentence:
                    self.show_sentence(s)
            )

            button.place(
                x=x,
                y=y,
                width=210,
                height=42
            )

            x += 220

            if x > 960:

                x = 735
                y += 50

    # ========================================================
    # STATUS
    # ========================================================

    def set_status(self, text):

        try:
            self.status_label.config(
                text=text
            )
        except:
            pass

    # ========================================================
    # MOUTH CLOSED
    # ========================================================

    def mouth_closed(self):

        self.canvas.coords(
            self.mouth,
            438,
            254,
            482,
            270
        )

        self.canvas.itemconfig(
            self.mouth,
            fill="#7c3f54"
        )

    # ========================================================
    # MOUTH OPEN
    # ========================================================

    def mouth_open(self):

        self.canvas.coords(
            self.mouth,
            430,
            248,
            490,
            282
        )

        self.canvas.itemconfig(
            self.mouth,
            fill="#5d263b"
        )

    # ========================================================
    # LIP SYNC
    # ========================================================

    def start_lip_sync(self):

        if self.mouth_running:
            return

        self.mouth_running = True

        self.animate_mouth()

    def animate_mouth(self):

        if not self.mouth_running:
            self.mouth_closed()
            return

        # Alternate mouth positions
        current = self.canvas.coords(
            self.mouth
        )

        if len(current) == 4:

            if current[3] - current[1] < 25:
                self.mouth_open()

            else:
                self.mouth_closed()

        self.mouth_animation_id = self.root.after(
            120,
            self.animate_mouth
        )

    def stop_lip_sync(self):

        self.mouth_running = False

        if self.mouth_animation_id:

            try:
                self.root.after_cancel(
                    self.mouth_animation_id
                )
            except:
                pass

            self.mouth_animation_id = None

        self.mouth_closed()

    # ========================================================
    # HAND ANIMATION
    # ========================================================

    def animate_hands(self, gesture="normal"):

        if gesture == "wave":

            self.wave_hand()

        elif gesture == "point":

            self.point_hand()

        elif gesture == "open":

            self.open_hands()

        elif gesture == "help":

            self.help_hands()

        else:

            self.normal_hands()

    # ========================================================
    # NORMAL HANDS
    # ========================================================

    def normal_hands(self):

        self.move_right_hand(
            680,
            555
        )

        self.move_left_hand(
            250,
            555
        )

    # ========================================================
    # OPEN HANDS
    # ========================================================

    def open_hands(self):

        self.move_right_hand(
            680,
            510
        )

        self.move_left_hand(
            250,
            510
        )

    # ========================================================
    # WAVE
    # ========================================================

    def wave_hand(self, count=0):

        if count >= 8:

            self.move_right_hand(
                680,
                555
            )

            return

        if count % 2 == 0:

            self.move_right_hand(
                700,
                470
            )

        else:

            self.move_right_hand(
                650,
                470
            )

        self.root.after(
            220,
            lambda: self.wave_hand(count + 1)
        )

    # ========================================================
    # POINT
    # ========================================================

    def point_hand(self):

        self.move_right_hand(
            700,
            490
        )

    # ========================================================
    # HELP HANDS
    # ========================================================

    def help_hands(self):

        self.move_left_hand(
            350,
            460
        )

        self.move_right_hand(
            580,
            460
        )

    # ========================================================
    # MOVE RIGHT HAND
    # ========================================================

    def move_right_hand(self, x, y):

        self.canvas.coords(
            self.right_forearm,
            665,
            450,
            x,
            y
        )

        self.update_hand_position(
            self.right_hand_parts,
            x,
            y,
            False
        )

    # ========================================================
    # MOVE LEFT HAND
    # ========================================================

    def move_left_hand(self, x, y):

        self.canvas.coords(
            self.left_forearm,
            265,
            450,
            x,
            y
        )

        self.update_hand_position(
            self.left_hand_parts,
            x,
            y,
            True
        )

    # ========================================================
    # UPDATE HAND
    # ========================================================

    def update_hand_position(
        self,
        parts,
        x,
        y,
        mirror
    ):

        # Instead of rebuilding complicated robot geometry,
        # move the hand parts using their bounding boxes.

        # Palm
        if len(parts) >= 1:

            self.canvas.coords(
                parts[0],
                x - 35,
                y - 30,
                x + 35,
                y + 35
            )

        # Fingers
        finger_positions = [-25, -8, 9, 26]

        for i, offset in enumerate(
            finger_positions
        ):

            line_index = 1 + i * 2
            joint_index = line_index + 1

            if line_index >= len(parts):
                continue

            length = 48

            if i == 3:
                length = 38

            fx = x + offset

            end_y = y - length

            self.canvas.coords(
                parts[line_index],
                fx,
                y - 5,
                fx,
                end_y
            )

            if joint_index < len(parts):

                self.canvas.coords(
                    parts[joint_index],
                    fx - 7,
                    end_y - 7,
                    fx + 7,
                    end_y + 7
                )

        # Thumb
        thumb_index = 9

        if thumb_index < len(parts):

            direction = -1 if mirror else 1

            self.canvas.coords(
                parts[thumb_index],
                x + direction * 25,
                y + 10,
                x + direction * 48,
                y - 5
            )

    # ========================================================
    # SENTENCE -> GESTURE
    # ========================================================

    def choose_gesture(self, sentence):

        sentence = sentence.upper().strip()

        if "HI" in sentence:

            return "wave"

        if "NICE TO MEET" in sentence:

            return "open"

        if "HELP" in sentence:

            return "help"

        if "HOW ARE YOU" in sentence:

            return "open"

        if "MY NAME" in sentence:

            return "point"

        if "NICE DAY" in sentence:

            return "open"

        return "normal"

    # ========================================================
    # SHOW SENTENCE
    # ========================================================

    def show_sentence(self, sentence):

        sentence = sentence.upper().strip()

        if not sentence:
            return

        print()
        print("=" * 60)
        print("SENTENCE RECEIVED:")
        print(sentence)
        print("=" * 60)

        self.current_sentence = sentence

        self.current_label.config(
            text=sentence
        )

        self.set_status(
            "Playing sentence..."
        )

        gesture = self.choose_gesture(
            sentence
        )

        self.animate_hands(
            gesture
        )

        # Start mouth animation
        self.start_lip_sync()

        # Start TTS
        self.speak_text(sentence)

    # ========================================================
    # SPEAK FROM ENTRY
    # ========================================================

    def speak_from_entry(self):

        sentence = self.sentence_entry.get().strip()

        if not sentence:
            self.set_status(
                "Please type a sentence."
            )
            return

        self.show_sentence(
            sentence
        )

    # ========================================================
    # TEXT TO SPEECH
    # ========================================================

    def speak_text(self, text):

        if self.speaking:
            return

        self.speaking = True

        # Start lips immediately
        self.start_lip_sync()

        def speech_worker():

            try:

                if not TTS_AVAILABLE:

                    # If pyttsx3 is not installed,
                    # keep animation running briefly.
                    time.sleep(
                        max(
                            1.5,
                            len(text) * 0.05
                        )
                    )

                else:

                    engine = pyttsx3.init()

                    # Speech speed
                    engine.setProperty(
                        "rate",
                        155
                    )

                    # Volume
                    engine.setProperty(
                        "volume",
                        1.0
                    )

                    # Try to select a female voice
                    try:

                        voices = engine.getProperty(
                            "voices"
                        )

                        for voice in voices:

                            name = (
                                str(
                                    getattr(
                                        voice,
                                        "name",
                                        ""
                                    )
                                )
                                .lower()
                            )

                            if (
                                "female" in name
                                or "zira" in name
                                or "samantha" in name
                            ):

                                engine.setProperty(
                                    "voice",
                                    voice.id
                                )

                                break

                    except Exception:
                        pass

                    engine.say(text)
                    engine.runAndWait()
                    engine.stop()

            except Exception as error:

                print(
                    "TTS ERROR:",
                    error
                )

            finally:

                self.root.after(
                    0,
                    self.finish_speaking
                )

        threading.Thread(
            target=speech_worker,
            daemon=True
        ).start()

    # ========================================================
    # FINISH SPEAKING
    # ========================================================

    def finish_speaking(self):

        self.speaking = False

        self.stop_lip_sync()

        self.set_status(
            "Sentence animation complete."
        )

        print(
            "Sentence animation complete."
        )

        # Return hands
        self.root.after(
            400,
            self.normal_hands
        )

    # ========================================================
    # VOICE CONTROL
    # ========================================================

    def start_voice_control(self):

        if self.voice_running:
            return

        if not SPEECH_AVAILABLE:

            self.set_status(
                "speech_recognition is not installed."
            )

            print(
                "Install it using:"
            )

            print(
                "pip install SpeechRecognition PyAudio"
            )

            return

        self.voice_running = True

        self.listen_button.config(
            text="🎤 LISTENING...",
            state=tk.DISABLED
        )

        self.set_status(
            "Listening... Speak now."
        )

        threading.Thread(
            target=self.voice_worker,
            daemon=True
        ).start()

    # ========================================================
    # VOICE WORKER
    # ========================================================

    def voice_worker(self):

        recognizer = sr.Recognizer()

        try:

            with sr.Microphone() as source:

                print()
                print("=" * 60)
                print("VOICE CONTROL")
                print("Listening...")
                print("=" * 60)

                recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.8
                )

                audio = recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=10
                )

            self.root.after(
                0,
                lambda: self.set_status(
                    "Recognizing speech..."
                )
            )

            text = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            text = text.upper().strip()

            print(
                "Recognized:",
                text
            )

            self.root.after(
                0,
                lambda t=text:
                self.process_voice_sentence(t)
            )

        except sr.WaitTimeoutError:

            self.root.after(
                0,
                lambda:
                self.set_status(
                    "No speech detected. Try again."
                )
            )

        except sr.UnknownValueError:

            self.root.after(
                0,
                lambda:
                self.set_status(
                    "I could not understand. Try again."
                )
            )

        except sr.RequestError as error:

            print(
                "Speech recognition error:",
                error
            )

            self.root.after(
                0,
                lambda:
                self.set_status(
                    "Speech service error."
                )
            )

        except Exception as error:

            print(
                "VOICE ERROR:",
                error
            )

            self.root.after(
                0,
                lambda:
                self.set_status(
                    "Microphone error."
                )
            )

        finally:

            self.root.after(
                0,
                self.voice_finished
            )

    # ========================================================
    # PROCESS VOICE SENTENCE
    # ========================================================

    def process_voice_sentence(self, text):

        self.sentence_entry.delete(
            0,
            tk.END
        )

        self.sentence_entry.insert(
            0,
            text
        )

        self.show_sentence(
            text
        )

    # ========================================================
    # VOICE FINISHED
    # ========================================================

    def voice_finished(self):

        self.voice_running = False

        self.listen_button.config(
            text="🎤 START LISTENING",
            state=tk.NORMAL
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset_avatar(self):

        self.stop_lip_sync()

        self.speaking = False

        self.normal_hands()

        self.current_label.config(
            text=""
        )

        self.set_status(
            "Ready"
        )

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.root.mainloop()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AI FEMALE SIGN LANGUAGE ROBOT")
    print("=" * 60)

    avatar = SignLanguageAvatar()

    avatar.run()