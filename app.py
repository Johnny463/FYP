# from pytube import YouTube
import pytube as pt
import boto3
import os
import os
import json
import time
# from pydub import AudioSegment
url = 'https://www.youtube.com/watch?v=2B3nvBbmMnk  '
# url = 'https://www.youtube.com/watch?v=9blBiI5SqcI  '

yt = pt.YouTube(url)
t = yt.streams.filter(only_audio=True)
filename=t[0].download()
print(filename,"@@File downloaded")
# sound = AudioSegment.from_file(filename,format="mp4")
# sound.export("file.wav", format="wav")

s3 = boto3.resource('s3')
BUCKET = "jhonny-usman"
s3.Bucket(BUCKET).upload_file(os.path.join("/home/ubuntu",filename), "files/file.mp4")


def transcribe_file(job_name, file_uri, transcribe_client):
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp4',
        # MediaFormat='wav',
        # LanguageCode='en-US'
        # LanguageCode='en-IN'
        LanguageCode='hi-IN'
    )

    max_tries = 60
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                print(
                    f"Download the transcript from\n"
                    f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
                os.system(
                    f"curl '{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}' > file.json")
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)


def delete_job(job_name, transcribe_client):
    """
    Deletes a transcription job. This also deletes the transcript associated with
    the job.

    :param job_name: The name of the job to delete.
    :param transcribe_client: The Boto3 Transcribe client.
    """
    transcribe_client.delete_transcription_job(
            TranscriptionJobName=job_name)

def main():
    t1 = time.time()
    transcribe_client = boto3.client('transcribe')
    # file_uri = 's3://jhonny-usman/files/file.mp4'
    file_uri = 's3://jhonny-usman/files/file.mp4'
    # file_uri = '/home/vicky/jhonny_project/speech.wav'
    # file_uri = 'speech.wav'
    job_name="example22"
    transcribe_file(job_name, file_uri, transcribe_client)
    with open("file.json", "r") as f:
        file = json.load(f)
    print(file["results"]["transcripts"][0]["transcript"])
    with open("aws_output.txt","w") as f:
        f.write(file["results"]["transcripts"][0]["transcript"])
    option=input(f"Want to delete this job {job_name} y/n?")
    if option.lower()=="y":
        delete_job(job_name, transcribe_client)
    t2 = time.time()
    print(
        f"@@@ AWS Transcribe service takes {str(t2-t1)} seconds to convert speech.wav file into text")

if __name__ == '__main__':
    main()

