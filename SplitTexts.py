# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

# Read file and replace Nan values with empty strings. Nan are nulls
df = pd.read_csv("/nobackup4/murrell/dataPrepFinal/finalDataSets/FilteredTranslatedDecisionComplaintArgument18000.csv")
df = df.replace(np.nan, '', regex=True)
print("Rows in original data: " + str(len(df)))

print(df.columns)

# dfDecision is the dataset with all entries that have both English and Russian decisions
# Same things for complaints and inBetween on next lines
dfDecision = df[(df['documents '] != '') & (df['engldecis '] != '')]
print("Rows with English and Russian decision: " + str(len(dfDecision)))
dfComplaint = df[(df['complaint '] != '') & (df['englcomplaint '] != '')]
print("Rows with English and Russian complaint: " + str(len(dfComplaint)))
dfBetween = df[(df['inBetweenText '] != '') & (df['englargu '] != '')]
print("Rows with English and Russian between: " + str(len(dfBetween)))

#Finding intersections
df_int1 = pd.merge(dfDecision, dfComplaint, 'inner')
df_int2 = pd.merge(df_int1, dfBetween, 'inner')

print("Rows with English and Russian all cols: " + str(len(df_int2)))

#Output to cluster
#dfDecision.to_csv('/nobackup4/murrell/dataPrepFinal/finalDataSets/HasDecisions.csv', encoding='utf-8')
#dfComplaint.to_csv('/nobackup4/murrell/dataPrepFinal/finalDataSets/HasComplaints.csv', encoding='utf-8')
#dfBetween.to_csv('/nobackup4/murrell/dataPrepFinal/finalDataSets/HasBetween.csv', encoding='utf-8')
df_int2.to_csv('/nobackup4/murrell/dataPrepFinal/finalDataSets/finalLargeData.csv', encoding='utf-8')












