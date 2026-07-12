import urllib.request
import tarfile
import os
import glob
import csv

os.makedirs("librispeech_test", exist_ok=True)
url = "https://www.openslr.org/resources/12/dev-clean.tar.gz"
tarpath = "librispeech_test/dev-clean.tar.gz"

if not os.path.exists(tarpath):
    urllib.request.urlretrieve(url, tarpath)

with tarfile.open(tarpath) as t:
    t.extractall("librispeech_test")

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
    w.writerow(["path","sentence"])
    for flac in flacs:
        uid = os.path.basename(flac).replace(".flac","")
        w.writerow([flac, refs[uid]])
print(f"{len(flacs)} clips and references.csv written")
