import re
with open("transcription_manual/plenery_full_transcript.txt") as f:
text = f.read()
text = re.sub(r"[A-Z][A-Z\s\.]+:\s*", "", text)
text = re.sub(r"\([^)]*\)", "", text)
text = re.sub(r"\s+", " ", text).strip()
with open("transcription_manual/plenary_full_clean.txt", "w") as f:
f.write(text)
print("cleaned, saved to transcription_manual/plenary_full_clean.txt")
