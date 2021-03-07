# -*- coding: utf-8 -*-
import pandas as pd

stmReadyDB = "/nobackup4/murrell/DbData/SplitFilesForSTM/StemmedAllText.csv"

df1 = pd.read_csv(stmReadyDB)
df2 = df1.copy(deep=True)

# Renumbers bottom half so it remains sequential
df2['Unnamed: 0'] += len(df1)

# Adds 'B' to start of each filename to denote bottom half
df2['fileName'] = 'B' + df2['fileName'].astype('str')


# Extract column values for switching in bottom df
rusDecis = df2[['documents ']].copy(deep=True)
englDecis = df2[['engldecis ']].copy(deep=True)
rusComp = df2[['complaint ']].copy(deep=True)
englComp = df2[['englcomplaint ']].copy(deep=True)
rusArgue = df2[['inBetweenText ']].copy(deep=True)
englArgue = df2[['englbetween ']].copy(deep=True)

# Switch cols for bottom df
df2['documents '] = englDecis
df2['engldecis '] = rusDecis
df2['complaint '] = englComp
df2['englcomplaint '] = rusComp
df2['inBetweenText '] = englArgue
df2['englbetween '] = rusArgue

# append switched df to original
dfAppend = df1.append(df2)

# Write to csv
dfAppend.to_csv("/nobackup4/murrell/DbData/SplitFilesForSTM/DoubleSwitchStemmedAllText.csv", encoding='utf-8')




