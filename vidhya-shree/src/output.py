from nlp import clean_text
from tts import speak_text


def process_output(recognized_text):

    print("Original:", recognized_text)

    final_text = clean_text(recognized_text)

    print("Processed:", final_text)

    speak_text(final_text)

    return final_text


if __name__ == "__main__":

    recognized_text = "hello how are you"

    process_output(recognized_text)