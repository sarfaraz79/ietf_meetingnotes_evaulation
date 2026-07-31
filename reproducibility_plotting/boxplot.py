import pandas as pd
import matplotlib.pyplot as plt

MASTER_CSV_PATH="../reproducibility_results/reproducibility_master.csv"
df=pd.read_csv(MASTER_CSV_PATH)
clips=["idr","netconf","lamps","plenary_openmic","plenary_full"]
order_of_model=["tiny","tiny.en","base","base.en","small","small.en","medium","medium.en","large-v3","turbo"]
plt.figure(figsize=(12,8))
for name_of_clip in clips:
    means=[]
    stds=[]
    models_present=[]
    for m in order_of_model:
        subset=df[(df['clip']==name_of_clip)&(df['model']==m)]
        if len(subset)==0:
            continue
        present_models.append(m)
        means.append(subset["wer"].mean()*100)
        stds.append(subset["wer"].std()*100)
    plt.errorbar(present_models,means,yerr=stds,marker="o",capsize=4,label=name_of_clip)
    
plt.xticks(rotation=45)
plt.ylabel("Word Error Rate %")
plt.title("WER wrt model size with error bars of reproducibility")
plt.legend()
plt.grid(True,alpha=0.3)
plt.tight_layout()
plt.savefig("reproducibility.pdf")
plt.close()

#boxplot
plt.figure(figsize=7,6)
subset=df[(df["clip"]=="netconf")&(df["model"]=='medium')]
plt.boxplot(subset["wer"]*100,tick_labels=["netconf,medium"])
plt.ylabel("WER")
plt.title("WER distribution \n netocnf,medium on repeated runs")
plt.grid(True,alpha=0.3,axis="y")
plt.tight_layout()
plt.savefig("boxplot.pdf")
plt.close()

    