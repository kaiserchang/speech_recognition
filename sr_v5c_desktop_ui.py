import sys
import speech_recognition as sr
import threading
import queue
import time
from googletrans import Translator
import logging
import argparse
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
import pyqtgraph as pg

python


# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 創建隊列來存儲轉錄的文本和音頻數據
text_queue = queue.Queue()
audio_queue = queue.Queue()

# 全局變量，用於控制線程
running = True

class SignalEmitter(QObject):
    text_signal = pyqtSignal(str)
    audio_signal = pyqtSignal(np.ndarray)

signal_emitter = SignalEmitter()

def transcribe_audio(source_lang):
    r = sr.Recognizer()
    while running:
        try:
            with sr.Microphone() as source:
                logger.info("監聽中... (請說話)")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
                audio_queue.put(audio_data)
                try:
                    text = r.recognize_google(audio, language=source_lang)
                    logger.info(f"轉錄: {text}")
                    text_queue.put(text)
                except sr.UnknownValueError:
                    logger.warning("無法識別音頻，請再試一次")
                except sr.RequestError as e:
                    logger.error(f"無法從Google Speech Recognition服務獲得結果; {e}")
        except sr.WaitTimeoutError:
            logger.info("等待超時，未檢測到語音輸入")
        except Exception as e:
            logger.error(f"發生錯誤: {e}")
        time.sleep(0.1)

def process_text(target_langs):
    translator = Translator()
    while running:
        texts = []
        while not text_queue.empty() and len(texts) < 5:  # 批量處理最多5條消息
            texts.append(text_queue.get())
        
        if texts:
            try:
                for lang in target_langs:
                    translations = translator.translate(texts, dest=lang)
                    for text, trans in zip(texts, translations):
                        output = f"原文: {text}\n翻譯 ({lang}): {trans.text}\n---\n"
                        signal_emitter.text_signal.emit(output)
            except Exception as e:
                logger.error(f"翻譯過程中發生錯誤: {e}")
        
        time.sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("語音辨識和翻譯程式")
        self.setGeometry(100, 100, 800, 900)

        layout = QVBoxLayout()

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setYRange(-32768, 32767)  # 設置Y軸範圍為16位音頻的範圍
        self.curve = self.plot_widget.plot(pen='y')
        layout.addWidget(self.plot_widget)

        self.stop_button = QPushButton("停止程式")
        self.stop_button.clicked.connect(self.stop_program)
        layout.addWidget(self.stop_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        signal_emitter.text_signal.connect(self.update_text)
        signal_emitter.audio_signal.connect(self.update_plot)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_audio)
        self.timer.start(50)  # 每50毫秒更新一次

    def update_text(self, text):
        self.text_output.append(text)

    def update_plot(self, audio_data):
        self.curve.setData(audio_data)

    def update_audio(self):
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            signal_emitter.audio_signal.emit(audio_data)

    def stop_program(self):
        global running
        running = False
        self.close()

def main(source_lang, target_langs):
    global running
    
    app = QApplication(sys.argv)
    window = MainWindow()
    
    transcribe_thread = threading.Thread(target=transcribe_audio, args=(source_lang,))
    process_thread = threading.Thread(target=process_text, args=(target_langs,))
    
    transcribe_thread.start()
    process_thread.start()
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="語音識別和翻譯程式")
    parser.add_argument("--source", default="zh-TW", help="源語言代碼 (默認: zh-TW)")
    parser.add_argument("--target", nargs="+", default=["en", "ja"], help="目標語言代碼列表 (默認: en ja)")
    args = parser.parse_args()

    main(args.source, args.target)