from youtube_transcript_api import YouTubeTranscriptApi as yta
vid_id = "YrhlQB3mQFI"
# vid_id = "VOpETRQGXy0"
data=yta.get_transcript(vid_id)
print(data)
transcript=" "
for value in data:
    for key,val in value.items():
        if key=="text":
            transcript+=val
l=transcript.splitlines()
output=" ".join(l)
# print(output)
with open("usman.txt","w") as f:
    f.write(output)

