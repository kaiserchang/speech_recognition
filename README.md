## 即時語音辨識小程式

這是一個預備用於線上會議即時翻譯的先期測試小程式，旨在測試如何使用 `speech_recognition` 模組來實現語音辨識功能。本程式利用 Google 語音辨識 API（免費）來將語音轉換為文字，並在說話停頓後輸出辨識結果。
![圖片描述](https://kaiserchang.github.io/img/v4c_demo.jpg =50%)

## 功能

- 持續監聽麥克風的語音。
- 語音辨識並在說話停頓後輸出辨識結果。
- 支援中文和整句英文的語音輸入。

## 安裝

在使用本程式之前，請確保已安裝以下 Python 模組：

- `speechrecognition`
- `pyaudio`
- `pyttsx3`

你可以使用以下命令來安裝這些模組：

```bash
pip install speechrecognition pyaudio pyttsx3
```
或是直接安裝 requirements

```bash
pip install -r requirements.txt
```
## macOS 安裝注意事項

在 macOS 系統上，你可能需要安裝一些前置元件。可以使用 port 或 brew 來安裝必要的依賴：

```bash
brew install portaudio
```

## 使用方法

確保麥克風已正確連接並正常工作。
下載或克隆本專案。
在終端機中執行程式：

```bash
python sr_v1c.py
```

程式會立即監聽麥克風並在終端機即時輸出辨識結果。

## 說明
本程式主要設計用於中文語音的即時翻譯，但也能夠處理整句英文語音。語音辨識的準確性可能會受到環境噪音、麥克風質量和說話清晰度的影響。

## 參考資料
- speech_recognition 模組官方文檔
- Google 語音辨識 API 文檔
- [NeuralNine](https://github.com/NeuralNine) 的 [YouTube 教學影片](https://youtu.be/9GJ6XeB-vMg?si=Nrn_i7ViNVzqMqRI)

## 授權
本專案使用 MIT 授權。

