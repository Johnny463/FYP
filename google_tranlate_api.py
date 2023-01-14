from pydub import AudioSegment
from google.cloud import speech
import os, shutil
import os
import time
time1=time.time()
audio_directory = "audio_files"
t1 = 0 * 1000  # Works in milliseconds
t2 = 59 * 1000
i = 0
newAudio = AudioSegment.from_wav("speech.wav")
shutil.rmtree(audio_directory,ignore_errors=True)
os.mkdir(audio_directory)
while True:
    audio_length = newAudio.__len__()
    audio_segment = (audio_length/59000)
    newAudio_segment = newAudio[t1:t2]
    t1 = t2
    newAudio_segment.export(os.path.join(audio_directory,f'newspeech_{i}.wav'), format="wav")
    if t2 < audio_length:
        t2 = t2+59000
    else:
        break
    i = i+1
client = speech.SpeechClient.from_service_account_file('key.json')
try:
    os.remove("google_output1.txt")
except Exception as e:
    print(str(e))
listdir = os.listdir(audio_directory)
for i, _ in enumerate(listdir):
    file_processing_time=time.time()
    print(f"@@@ Converting file newspeech_{i}.wav into text by google API.......")
    print(f"@@@ converting {str(i+1)} out of {str(len(listdir))} files.............")
    file_path = os.path.join(audio_directory, f"newspeech_{i}.wav")
    with open(file_path,'rb')as f:
        mp3_data=f.read()
    audio_file=speech.RecognitionAudio(content=mp3_data)
    config=speech.RecognitionConfig(
        sample_rate_hertz=44100,
        enable_automatic_punctuation=True,
        language_code="en-US",
        audio_channel_count=2
    )
    response = client.recognize(
        config=config,
        audio=audio_file
    )
    print(response.results)
    with open("google_output1.txt","a+") as f:
        f.write(str(response.results))
    t2= time.time()
    print(
        f"@@@ Google API takes {str(t2-file_processing_time)} seconds to convert newspeech_{i}.wav file into text")
t2 = time.time()
print(
    f"Total Time for doing this entire conversion is {str(t2-time1)} seconds")

