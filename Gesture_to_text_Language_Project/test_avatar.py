import cv2
from avatar import Avatar

avatar = Avatar()

# Test different signs one by one
signs = [
    "HELLO",
    "THANK_YOU",
    "YES",
    "NO",
    "PLEASE",
    "HELP",
    "GOOD",
    "BAD",
    "I_LOVE_YOU",
    "STOP",
]

index = 0
avatar.update(signs[index])

while True:

    frame = cv2.imread("test_background.jpg")

    if frame is None:
        frame = 255 * __import__("numpy").ones(
            (600, 1000, 3),
            dtype="uint8"
        )

    avatar.render(
        frame,
        x=650,
        y=50,
        w=300,
        h=500
    )

    cv2.putText(
        frame,
        f"Testing: {signs[index]}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2
    )

    cv2.putText(
        frame,
        "N = next sign | Q = quit",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 0),
        2
    )

    cv2.imshow("AI Avatar Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("n"):
        index = (index + 1) % len(signs)
        avatar.update(signs[index])

    elif key == ord("q"):
        break

cv2.destroyAllWindows()