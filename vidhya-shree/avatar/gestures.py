def show_gesture(self, gesture_name):

    gesture_name = gesture_name.upper()

    print("Gesture received:", gesture_name)

    if gesture_name == "HELLO":
        print("Performing HELLO gesture")
        self.wave()

    elif gesture_name == "THANK YOU":
        print("Performing THANK YOU gesture")
        self.thank_you()

    elif gesture_name == "YES":
        print("Performing YES gesture")
        self.yes()

    elif gesture_name == "NO":
        print("Performing NO gesture")
        self.no()

    elif gesture_name == "HELP":
        print("Performing HELP gesture")
        self.help()

    else:
        print("Gesture not available:", gesture_name)