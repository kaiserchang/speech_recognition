import speech_recognition as sr
import pyttsx3
import time

recognizer = sr.Recognizer()

def recognize_speech(language="zh-TW"):
    try:
        with sr.Microphone() as mic:
            print("調整環境噪音...")
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            print("請說話...")
            audio = recognizer.listen(mic, timeout=5, phrase_time_limit=5)
            
            print("正在處理您的語音...")
            text = recognizer.recognize_google(audio, language=language)
            text = text.lower()
            
            print(f"辨識結果: {text}")
            return text
            
    except sr.WaitTimeoutError:
        print("沒有檢測到語音，請再試一次。")
    except sr.UnknownValueError:
        print("無法理解音頻，請再試一次。")
    except sr.RequestError as e:
        print(f"無法從Google語音辨識服務取得結果；{e}")
    except Exception as e:
        print(f"發生錯誤：{e}")
    
    return None

def main():
    print("語音辨識程式啟動")
    print("請確保您的麥克風已連接並正常工作")
    
    try:
        while True:
            print("\n準備開始新的語音辨識...")
            result = recognize_speech(language="zh-TW")
            if result:
                print("您可以繼續說話，或按Ctrl+C結束程式")
            else:
                print("未能成功辨識語音，稍後將再次嘗試")
            time.sleep(2)  # 暫停2秒後再次嘗試

    except KeyboardInterrupt:
        print("\n程式被使用者中斷。")

    finally:
        print("程式結束。")

if __name__ == "__main__":
    try:
        with sr.Microphone() as mic:
            print("成功初始化麥克風")
        main()
    except Exception as e:
        print(f"無法初始化麥克風；錯誤訊息：{e}")
        print("請確保您的電腦有可用的麥克風（內建或外接）。")
        print("程式無法繼續執行。")