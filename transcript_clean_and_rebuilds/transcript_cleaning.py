import re

with open("transcription_manual/plenery_full_transcript.txt") as f:
    text =f.read()

text=re.sub(r"[A-Z][A-Z\s\.]+:\s*","",text) #for remvoing the speaker labels
text = re.sub(r"\([^)]*\)", "", text)#for removing the applause in transcript
text=re.sub(r"\s+"," ",text).strip()#for the whitespaces

with open("transcription_manual/plenery_clean_transcript.txt", "w") as f:
    f.write(text)
    
print("done")