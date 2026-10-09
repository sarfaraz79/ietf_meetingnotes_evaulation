import matplotlib.pyplot as plt
import numpy as np

def main():
    groups=["lamps(SEC)","netconf(OPS)","idr(RTG)"]
    wer=[18.3,28.4,31]
    sbert=[89.5,67.6,67.2]
    trr=[84,24,45]
    
    x=np.arange(len(groups))
    width=0.2
    fig,ax=plt.subplots()
    bars_wer=ax.bar(x-width,wer,width,label="WER")
    bars_sbert=ax.bar(x,sbert,width,label="SBERT")
    bars_trr=ax.bar(x+width,trr,width,label="TRR")
    
    for bars in (bars_wer,bars_sbert,bars_trr):
        for bar in bars:
            ax.text(bar.get_x()+bar.get_width()/2,bar.get_height(),f"{bar.get_height():.1f}",ha="center",va="bottom")
    ax.set_xticks
    ax.set_xticklabels(groups)
    ax.set_ylabel("Percentage")
    ax.set_ylim(0,100)
    ax.set_title("Performance Comparison of Different Methods")
    ax.legend()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig("preliminary_metrics.pdf")
    plt.close()

if __name__=="__main__":
    main()