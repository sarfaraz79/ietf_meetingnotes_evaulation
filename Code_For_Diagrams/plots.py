#libraries used
#pandas
#matplotlib
#numpy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

order_of_model=["tiny","tiny.en","base","base.en","small","small.en","medium","medium.en","large-v3","turbo"]#the model's based on their sizes
df=pd.read_csv("master_results/master_results.csv")#reading the csv file
df["model"]=pd.Categorical(df["model"],categories=order_of_model,ordered=True)