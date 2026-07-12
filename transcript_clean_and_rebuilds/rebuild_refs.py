import glob 
import os 
import csv

base = "librispeech_test/LibriSpeech/dev-clean"
refs = {}
for trans in glob.glob(f"{base}/*/*/*.trans.txt"):
    with open(trans) as f:
        for line in f:
            uid, text = line.strip().split(" ", 1)
            refs[uid] = text
flacs = sorted(glob.glob(f"{base}/*/*/*.flac"))[:200]
with open("librispeech_test/references.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["path", "sentence"])
    for flac in flacs:
        uid = os.path.basename(flac).replace(".flac", "")
        w.writerow([flac, refs[uid]])

print(f"rebuilt references.csv with {len(flacs)} clips")
