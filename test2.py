from pydub import AudioSegment
t1 = 0 * 1000  # Works in milliseconds
t2 = 59 * 1000
i=1
newAudio = AudioSegment.from_wav("speech.wav")
while True:
    audio_length = newAudio.__len__()
    audio_segment = (audio_length/59000)
    newAudio_segment = newAudio[t1:t2]
    t1=t2
    newAudio_segment.export(f'audio_files/newspeech_{i}.wav', format="wav")
    if t2<audio_length:
        t2=t2+59000
    else:
        break
    i=i+1
