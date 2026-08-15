import cv2
import numpy as np
import time


class Avatar:

    def __init__(self):

        self.current_sign = "IDLE"

        self.last_update = time.perf_counter()

        self.animation_start = time.perf_counter()

    # ---------------------------------------------------------
    # Update avatar
    # ---------------------------------------------------------

    def update(self, sign):

        if sign:
            self.current_sign = sign.upper()
        else:
            self.current_sign = "IDLE"

        self.last_update = time.perf_counter()
        self.animation_start = time.perf_counter()

    # ---------------------------------------------------------
    # Current avatar state
    # ---------------------------------------------------------

    def state(self):

        return self.current_sign

    # ---------------------------------------------------------
    # Draw face
    # ---------------------------------------------------------

    def draw_face(
        self,
        frame,
        cx,
        cy
    ):

        skin = (220, 190, 160)

        # Face
        cv2.ellipse(
            frame,
            (cx, cy),
            (70, 85),
            0,
            0,
            360,
            skin,
            -1
        )

        # Face outline
        cv2.ellipse(
            frame,
            (cx, cy),
            (70, 85),
            0,
            0,
            360,
            (255, 255, 255),
            2
        )

        # Hair
        cv2.ellipse(
            frame,
            (cx, cy - 55),
            (72, 40),
            0,
            180,
            360,
            (40, 40, 40),
            -1
        )

        # Eyes
        cv2.circle(
            frame,
            (cx - 25, cy - 5),
            6,
            (20, 20, 20),
            -1
        )

        cv2.circle(
            frame,
            (cx + 25, cy - 5),
            6,
            (20, 20, 20),
            -1
        )

        # Nose
        cv2.line(
            frame,
            (cx, cy),
            (cx - 5, cy + 20),
            (90, 70, 60),
            2
        )

        # Mouth
        elapsed = time.perf_counter() - self.last_update

        if elapsed < 2:

            mouth = int(
                8 + 6 * abs(np.sin(elapsed * 10))
            )

            cv2.ellipse(
                frame,
                (cx, cy + 45),
                (18, mouth),
                0,
                0,
                360,
                (60, 40, 40),
                -1
            )

        else:

            cv2.line(
                frame,
                (cx - 15, cy + 45),
                (cx + 15, cy + 45),
                (60, 40, 40),
                2
            )

    # ---------------------------------------------------------
    # Draw body
    # ---------------------------------------------------------

    def draw_body(
        self,
        frame,
        cx,
        top
    ):

        cv2.rectangle(
            frame,
            (cx - 65, top),
            (cx + 65, top + 190),
            (90, 130, 180),
            -1
        )

    # ---------------------------------------------------------
    # Draw HELLO
    # ---------------------------------------------------------

    def draw_hello(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        # Arm
        cv2.line(
            frame,
            (cx + 45, top + 30),
            (cx + 100, top - 40),
            skin,
            18
        )

        # Waving hand
        hand_x = cx + 105
        hand_y = top - 50

        cv2.circle(
            frame,
            (hand_x, hand_y),
            25,
            skin,
            -1
        )

        # Moving fingers
        wave = int(8 * np.sin(t * 8))

        for i in range(4):

            fx = hand_x - 18 + i * 12

            cv2.line(
                frame,
                (fx, hand_y - 15),
                (fx + wave, hand_y - 45),
                skin,
                7
            )

    # ---------------------------------------------------------
    # Draw YES
    # ---------------------------------------------------------

    def draw_yes(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        cv2.line(
            frame,
            (cx + 45, top + 30),
            (cx + 100, top + 5),
            skin,
            18
        )

        # Thumb
        cv2.line(
            frame,
            (cx + 100, top + 5),
            (cx + 105, top - 35),
            skin,
            12
        )

        cv2.circle(
            frame,
            (cx + 105, top - 40),
            15,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw NO
    # ---------------------------------------------------------

    def draw_no(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        movement = int(
            15 * np.sin(t * 7)
        )

        cv2.line(
            frame,
            (cx - 40, top + 30),
            (cx - 100 + movement, top - 5),
            skin,
            18
        )

        cv2.circle(
            frame,
            (cx - 105 + movement, top - 10),
            25,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw STOP
    # ---------------------------------------------------------

    def draw_stop(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        # Raised arm
        cv2.line(
            frame,
            (cx + 45, top + 40),
            (cx + 90, top - 35),
            skin,
            20
        )

        # Open palm
        cv2.rectangle(
            frame,
            (cx + 70, top - 80),
            (cx + 125, top - 25),
            skin,
            -1
        )

        # Fingers
        for i in range(5):

            fx = cx + 75 + i * 11

            cv2.line(
                frame,
                (fx, top - 55),
                (fx, top - 95),
                skin,
                7
            )

    # ---------------------------------------------------------
    # Draw GOOD
    # ---------------------------------------------------------

    def draw_good(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        cv2.line(
            frame,
            (cx + 45, top + 30),
            (cx + 105, top),
            skin,
            18
        )

        # Thumb up
        cv2.line(
            frame,
            (cx + 105, top),
            (cx + 105, top - 45),
            skin,
            12
        )

        cv2.circle(
            frame,
            (cx + 105, top - 50),
            15,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw BAD
    # ---------------------------------------------------------

    def draw_bad(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        movement = int(
            10 * np.sin(t * 6)
        )

        cv2.line(
            frame,
            (cx + 45, top + 30),
            (cx + 105, top - 10 + movement),
            skin,
            18
        )

        cv2.circle(
            frame,
            (cx + 110, top - 15 + movement),
            24,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw THANK YOU
    # ---------------------------------------------------------

    def draw_thank_you(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        movement = int(
            20 * np.sin(t * 4)
        )

        # Hand moves outward from mouth
        cv2.line(
            frame,
            (cx + movement, top + 20),
            (cx + 90 + movement, top + 10),
            skin,
            18
        )

        cv2.circle(
            frame,
            (cx + 95 + movement, top + 5),
            23,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw PLEASE
    # ---------------------------------------------------------

    def draw_please(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        movement = int(
            12 * np.sin(t * 5)
        )

        # Hand on chest
        cv2.circle(
            frame,
            (cx + movement, top + 65),
            35,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw HELP
    # ---------------------------------------------------------

    def draw_help(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        # Both hands raised
        cv2.line(
            frame,
            (cx - 45, top + 40),
            (cx - 105, top - 25),
            skin,
            18
        )

        cv2.line(
            frame,
            (cx + 45, top + 40),
            (cx + 105, top - 25),
            skin,
            18
        )

        cv2.circle(
            frame,
            (cx - 110, top - 30),
            23,
            skin,
            -1
        )

        cv2.circle(
            frame,
            (cx + 110, top - 30),
            23,
            skin,
            -1
        )

    # ---------------------------------------------------------
    # Draw I LOVE YOU
    # ---------------------------------------------------------

    def draw_i_love_you(
        self,
        frame,
        cx,
        top,
        t
    ):

        skin = (220, 190, 160)

        # Raised hand
        cv2.line(
            frame,
            (cx + 40, top + 35),
            (cx + 95, top - 30),
            skin,
            18
        )

        cv2.circle(
            frame,
            (cx + 100, top - 40),
            25,
            skin,
            -1
        )

        # Three raised fingers representation
        for i in range(3):

            fx = cx + 85 + i * 12

            cv2.line(
                frame,
                (fx, top - 40),
                (fx, top - 75),
                skin,
                7
            )

    # ---------------------------------------------------------
    # Render Avatar
    # ---------------------------------------------------------

    def render(
        self,
        frame,
        x=500,
        y=160,
        w=300,
        h=430
    ):

        frame_height, frame_width = frame.shape[:2]

        # Keep avatar inside frame
        x = max(
            10,
            min(x, frame_width - w - 10)
        )

        y = max(
            10,
            min(y, frame_height - h - 10)
        )

        # -----------------------------------------------------
        # Avatar panel
        # -----------------------------------------------------

        panel = frame.copy()

        cv2.rectangle(
            panel,
            (x, y),
            (x + w, y + h),
            (25, 25, 25),
            -1
        )

        cv2.rectangle(
            panel,
            (x, y),
            (x + w, y + h),
            (255, 255, 255),
            2
        )

        cv2.putText(
            panel,
            "AI AVATAR",
            (x + 80, y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        # -----------------------------------------------------
        # Avatar position
        # -----------------------------------------------------

        cx = x + w // 2

        head_y = y + 125

        body_y = y + 215

        # -----------------------------------------------------
        # Face + body
        # -----------------------------------------------------

        self.draw_face(
            panel,
            cx,
            head_y
        )

        self.draw_body(
            panel,
            cx,
            body_y
        )

        # Animation time
        t = time.perf_counter() - self.animation_start

        sign = self.current_sign.upper()

        # -----------------------------------------------------
        # Perform sign
        # -----------------------------------------------------

        if sign == "HELLO":

            self.draw_hello(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "YES":

            self.draw_yes(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "NO":

            self.draw_no(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "STOP":

            self.draw_stop(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "GOOD":

            self.draw_good(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "BAD":

            self.draw_bad(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "THANK_YOU":

            self.draw_thank_you(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "PLEASE":

            self.draw_please(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "HELP":

            self.draw_help(
                panel,
                cx,
                body_y,
                t
            )

        elif sign == "I_LOVE_YOU":

            self.draw_i_love_you(
                panel,
                cx,
                body_y,
                t
            )

        # -----------------------------------------------------
        # Display current sign
        # -----------------------------------------------------

        label = sign.replace(
            "_",
            " "
        )

        cv2.putText(
            panel,
            label,
            (x + 20, y + h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        # -----------------------------------------------------
        # Blend avatar
        # -----------------------------------------------------

        cv2.addWeighted(
            panel,
            0.95,
            frame,
            0.05,
            0,
            frame
        )