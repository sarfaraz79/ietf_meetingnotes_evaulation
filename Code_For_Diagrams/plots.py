#libraries used
#pandas
#matplotlib
#numpy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#for librispeech baseline results
order_of_model=["tiny","tiny.en","base","base.en","small","small.en","medium","medium.en","large-v3","turbo"]#the model's based on their sizes
df=pd.read_csv("../master_results/master_results.csv")#reading the csv file
df["model"]=pd.Categorical(df["model"],categories=order_of_model,ordered=True)
df=df.sort_values("model")

base=pd.read_csv("../librispeech_model_test_results/baseline_results.csv")#reading the baseline results csv file
base_order_of_model=["tiny","base","small","medium","large-v3"]
base["model"]=pd.Categorical(base["model"],categories=base_order_of_model,ordered=True)
base=base.sort_values("model")
plt.figure(figsize=(8,5))
plt.plot(base["model"],base["WER"]*100,marker="o",linewidth=2,color="blue")#plotting the baseline results
plt.title("WER on LibriSpeech Test Set")
plt.xlabel("Whisper Model")
plt.ylabel("WER")
plt.grid(True,alpha=0.3)
for x,y in zip(base["model"],base["WER"]*100):
    plt.text(x,y+0.2,f"{y:.1f}",ha="center",fontsize=9)#adding the WER values on the plot
plt.tight_layout()
plt.savefig("baseline_results_librispeech.pdf")#saving the plot
plt.close()

