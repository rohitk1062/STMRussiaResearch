# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

path = '/nobackup4/murrell/dataPrepFinal/finalDataSets/CompleteData.csv'
df = pd.read_csv(path)

lenBf = len(df)
df = df[(df['argument'].str.len() >= 100) & (df['englargument'].str.len() >= 100) & (df['decision'].str.len() >= 100) & (df['engldecision'].str.len() >= 100) & (df['complaint'].str.len() >= 100) & (df['englcomplaint'].str.len() >= 100)]
lenAf = len(df)
lenChange = lenBf - lenAf

print("change in rows: " + str(lenChange))
df.to_csv(path, encoding='utf-8', index=False)

