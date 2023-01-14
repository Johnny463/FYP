from pydub import AudioSegment
t1 = 0 * 1000  # Works in milliseconds
t2 = 59 * 1000
newAudio = AudioSegment.from_wav("speech.wav")
newAudio.export('newspeech.wav', format="wav")
