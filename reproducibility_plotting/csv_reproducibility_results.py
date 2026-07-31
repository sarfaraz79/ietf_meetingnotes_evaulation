#external libraries used
#os,re,glob,csv
import os
import re
import glob
import csv

ROOT="reproducibility_results"
CLIPS=["idr","netconf","lamps","plenary_opemic","plenary_full"]

def extracting_run_number(path):
    m=re.search("r_wer_run(\d+)\.txt",path)
    return int(m.group(1)) if m else None

def wer_extraction(path):
    with open(path) as f:
        text=f.read()
    m=re.search(r"Word Error Rate:\s*([0-9.]+)",text)
    return float(m.group(1)) if m else None

rows=[]
for clip in clips:
    model_directories=glob.glob(os.path.join(ROOT,clip,"*"))
    for model_directories in model_directories:
        name_of_model=os.path.basename(model_directories)
        wer_files=glob.glob(os.path.join(model_directories,"*_wer_run*.txt"))
        for path in wer_files:
            wer=wer_extraction(path)
            run=extracting_run_number(path)
            if wer is None or run is None:
                continue
            rows.append([clip,model_name,run,wer])

rows.sort(key=lambda r:(CLIPS.index(r[0]),r[1],r[2]))
output_path=os.path.join(ROOT,"reproducibility_master.csv")
with open(output_path,"w",newline="") as f:
    w=csv.write(f)
    w.writerow(["clip","model","run","wer"])
    w.writerows(rows)

print("clip,model,run,wer")
for row in rows:
    print(f"{row[0]},{row[2]},{row[3]}")