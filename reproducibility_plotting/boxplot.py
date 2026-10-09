import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cm=1/2.54
DIRECTORY=os.path.dirname(os.path.abspath(__file__))
MASTER_CSV_PATH=os.path.join(DIRECTORY,"..","reproducibility_results","reproducibility_master.csv")
df=pd.read_csv(MASTER_CSV_PATH)
y_max=(df["wer"].max()*100)+5
clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
order_of_model=["tiny","tiny.en","base","base.en","small","small.en","medium","medium.en","large-v3","turbo"]
plt.figure(figsize=(12*cm,7.5*cm))
for name_of_clip in clips:
    means=[]
    stds=[]
    models_present=[]
    for m in order_of_model:
        subset=df[(df['clip']==name_of_clip)&(df['model']==m)]
        if len(subset)==0:
            continue
        models_present.append(m)
        means.append(subset["wer"].mean()*100)
        stds.append(subset["wer"].std()*100)
    plt.errorbar(models_present,means,yerr=stds,marker="o",capsize=4,label=name_of_clip)
    
plt.xticks(rotation=45,fontsize=8)
plt.ylabel("Word Error Rate %",fontsize=9)
plt.title("WER wrt model size with error bars of reproducibility")
plt.legend()
plt.grid(True,alpha=0.3)
plt.ylim(bottom=0, top=y_max)
plt.yticks(np.arange(0,y_max+1,30),fontsize=12)
plt.tight_layout()
plt.savefig("reproducibility.pdf")
plt.close()

#boxplot
plt.figure(figsize=(6*cm,6*cm))
subset=df[(df["clip"]=="netconf")&(df["model"]=='medium')]
plt.boxplot(subset["wer"]*100,tick_labels=["netconf,medium"])
plt.ylabel("WER",fontsize=9)
plt.title("WER distribution \n netocnf,medium on repeated runs",fontsize=10)
plt.grid(True,alpha=0.3,axis="y")
plt.ylim(bottom=0, top=y_max)
plt.yticks(np.arange(0,y_max+1,30),fontsize=12)
plt.tight_layout()
plt.savefig("boxplot.pdf")
plt.close()

for name_of_clip in clips:
    plt.figure(figsize=(12*cm,7.5*cm))
    to_plot=[]
    models_present=[]   
    for model in order_of_model:
        subset=df[(df["clip"]== name_of_clip)&(df["model"]== model)]
        if len(subset)==0:
            continue
        to_plot.append(subset["wer"]*100)
        models_present.append(model)
    plt.boxplot(to_plot,tick_labels=models_present)
    plt.xticks(rotation=45,fontsize=8)
    plt.ylabel("WER",fontsize=9)
    plt.title("WER distribution",fontsize=10)
    plt.grid(True,alpha=0.3,axis="y")
    plt.ylim(bottom=0, top=y_max)
    plt.yticks(np.arange(0,y_max+1,30),fontsize=12)
    plt.tight_layout()
    plt.savefig(f"boxplot_{name_of_clip}.pdf")
    plt.close()