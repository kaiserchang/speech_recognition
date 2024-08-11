import speech_recognition as sr
import threading
import queue
import time
from googletrans import Translator

# 創建一個隊列來存儲轉錄的文本
text_queue = queue.Queue()

def transcribe_audio():
    r = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("監聽中... (請說話)")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                try:
                    text = r.recognize_google(audio, language="zh-TW")
                    print(f"轉錄: {text}")
                    text_queue.put(text)
                except sr.UnknownValueError:
                    print("無法識別音頻，請再試一次")
                except sr.RequestError as e:
                    print(f"無法從Google Speech Recognition服務獲得結果; {e}")
        except sr.WaitTimeoutError:
            print("等待超時，未檢測到語音輸入")
        except Exception as e:
            print(f"發生錯誤: {e}")
        time.sleep(1)

def process_text():
    translator = Translator()
    while True:
        if not text_queue.empty():
            text = text_queue.get()
            # 進行翻譯
            try:
                translated = translator.translate(text, src='zh-tw', dest='en')
                print(f"翻譯 (英文): {translated.text}")
                
                # 你可以在這裡添加更多的目標語言
                translated_ja = translator.translate(text, src='zh-tw', dest='ja')
                print(f"翻譯 (日文): {translated_ja.text}")
                
            except Exception as e:
                print(f"翻譯過程中發生錯誤: {e}")
        time.sleep(0.1)

# 啟動轉錄線程
transcribe_thread = threading.Thread(target=transcribe_audio)
transcribe_thread.daemon = True
transcribe_thread.start()

# 啟動文本處理線程
process_thread = threading.Thread(target=process_text)
process_thread.daemon = True
process_thread.start()

print("語音辨識和翻譯程式已啟動")
print("說話時，您的語音將被轉錄並翻譯")
print("按 Ctrl+C 可以停止程式")

# 主程序保持運行
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n程序被用戶中斷")