no# 即時翻譯功能前置小程式

這是一個用於線上會議即時翻譯的 Python 小程式，旨在演示如何使用 `speech_recognition` 模組來實現語音辨識功能。本程式利用 Google 語音辨識 API（免費）來將語音轉換為文字，並在說話停頓後輸出辨識結果。

## 功能

- 持續監聽麥克風的語音。
- 語音辨識並在說話停頓後輸出辨識結果。
- 支援中文和整句英文的語音輸入。

## 安裝

在使用本程式之前，請確保已安裝以下 Python 模組：

- `speechrecognition`
- `pyaudio`

你可以使用以下命令來安裝這些模組：

```bash
pip install speechrecognition pyaudio

# macOS 安裝注意事項

在 macOS 系統上，你可能需要安裝一些前置元件。可以使用 port 或 brew 來安裝必要的依賴：

```bash
brew install portaudio
