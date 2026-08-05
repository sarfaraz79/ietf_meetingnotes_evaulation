import os
import glob
import csv 
import re

def get_wer(path): #will reach wer file and pull the path
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        text =f.read()
    m=re.search(r"Word Error Rate:\s*([0-9.]+)", text)
    return float(m.group(1)) if m else ""


def get_trr(path):#will read trr file and give number
    if not os.path.exists(path):
        return ""
    with open(path) as f:
        text =f.read()
    m=re.search(r"TRR:\s*([0-9.]+)", text)
    return round(float(m.group(1)), 4) if m else ""

MODELS = ["tiny","tiny.en","base","base.en","small","small.en",
          "medium","medium.en","large-v3","turbo"]
rows = []
CLIPS = ["idr","netconf","lamps","plenary_openmic"]
for clip in CLIPS:
    for model in MODELS:
        wer = get_wer(f"clips_results/{clip}/{model}_wer.txt")
        trr = get_trr(f"clips_results/{clip}/{model}_trr.txt")
        rows.append([clip, model, wer, trr])
        
for model in MODELS:
    wer=get_wer(f"plenary_full_results/{model}_wer.txt")
    trr=get_trr(f"plenary_full_results/{model}_trr.txt")
    rows.append(["plenary_full",model,wer,trr])


with open("model_tabular_result/all_models_results.csv", "w", newline="") as f:
    w =csv.writer(f)
    w.writerow(["clip","model","wer","trr"])
    w.writerows(rows)

print()
for clip in CLIPS + ["plenary_full"]:
    print(clip)
    for row in rows:
        if row[0] == clip:
            print(f" {row[1]:12} wer {row[2]}  trr {row[3]}")
    print()
