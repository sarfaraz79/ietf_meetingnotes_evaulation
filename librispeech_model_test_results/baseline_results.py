#libraries used 
#os 
#re
#csv
#glob

import os
import re
import csv
import glob

folder="librispeech_model_test_results"
files=glob.glob(os.path.join(folder,"baseline_*"))
rows=[]
for file in files:
    with open(file) as f:
        text=f.read()
        model=os.path.basename(file).replace("baseline_","").replace(".txt","")
        m=re.search(r"wer\s*([0-9.]+)",text)
        if m:
            wer=float(m.group(1))
            rows.append([model,wer])
        else:
            print(f"WER not found in {file}")
order=["tiny","tiny.en","base","base.en","small","small.en","medium","medium.en","large-v3","turbo"]#the model's based on their sizes
rows.sort(key=lambda r:order.index(r[0]) if r[0] in order else 99)#sorting the rows based on the order of models
output_file=os.path.join(folder,"baseline_results.csv")
with open(output_file,"w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["model","WER"])
    for model in order:
        for row in rows:
            if row[0]==model:
                writer.writerow(row)
        