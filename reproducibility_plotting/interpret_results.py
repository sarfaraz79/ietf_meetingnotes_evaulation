#external libraries used
#pandas
import pandas as pd
df=pd.read_csv("reproducibility_results/reproducibility_master.csv")
summary_rows=[]
for clip in df["clip"].unique():
    for model in df[df["clip"]==clip]["model"].unique():
        subset=df[(df["clip"]==clip)&(df["model"]==model)]
        wers=subset["wer"]
        mean=wers.mean()
        std=wers.std()
        minimum_wer=wers.min()
        maximum_wer=wers.max()
        n=len(wers)
        spread=maximum_wer-minimum_wer
        summary_rows.append({
            "clip":clip,"model":model,"n_runs":n,"mean_wer":round(mean,4),"standard_wer":round(std,4),"minimum_wer":round(minimum_wer,4),"maximum_wer":round(maximum_wer,4),"spread":round(spread,4)
        })
summary_df=pd.DataFrame(summary_rows)
summary_df.to_csv("reproducibility_summary.csv",index=False)
overall_std=summary_df["standard_wer"].mean()
maximum_spread_row=summary_df.loc[summary_df["spread"].idxmax()]
minimum_spread_row=summary_df.loc[summary_df["spread"].idxmin()]
print(f"Avg standard deviation across all the model combinations:{overall_std:.4f}")
print(f"Largest spread:{maximum_spread_row['clip']}/{maximum_spread_row['model']},"f"spread={maximum_spread_row['spread']:.4f}")
print(f"Smallest spread:{minimum_spread_row['clip']}/{minimum_spread_row['model']},"f"spread={minimum_spread_row['spread']:.4f}")