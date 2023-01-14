import os
import speech_recognition as sr
import json
# import ffmpeg
# command2mp3 = "ffmpeg -i speech.mp4 speech.mp3"
# command2wav = "ffmpeg -i speech.mp3 speech.wav"
# os.system(command2mp3)
# os.system(command2wav)
r = sr.Recognizer()
with sr.AudioFile("speech.wav") as source:
    audio = r.record(source, duration=120)
print(r.recognize_google(audio))
# sFinalResult=r.recognize_google(audio,language='en-IN',show_all=True)
# response = json.dumps(sFinalResult, ensure_ascii=False).encode('utf8')
# print(r.recognize_google(audio,language='fr-FR', show_all=True))
# print(r.recognize_google(audio,language='en-IN', show_all=True))
