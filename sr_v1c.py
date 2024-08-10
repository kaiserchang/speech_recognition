import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()

def recognize_speech(language="zh-TW"):
    try:
        with sr.Microphone() as mic:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("Listening...")
            audio = recognizer.listen(mic)
            
            # 使用指定的語言進行語音識別
            text = recognizer.recognize_google(audio, language=language)
            text = text.lower()
            
            print(f"Recognized: {text}")
            
    except sr.UnknownValueError:
        print("Could not understand audio, trying again...")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

try:
    while True:
        recognize_speech(language="zh-TW")  # 使用繁體中文識別

except KeyboardInterrupt:
    print("Process interrupted by user.")

finally:
    print("Program terminated.")