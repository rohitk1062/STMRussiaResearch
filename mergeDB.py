# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# Read files
smallFile = '/nobackup4/murrell/dataPrepFinal/finalDataSets/finalSmallerData.csv'
largeFile = '/nobackup4/murrell/dataPrepFinal/finalDataSets/finalLargeData.csv'

smallDf = pd.read_csv(smallFile)
largeDf = pd.read_csv(largeFile)

print("rows in small file: " + str(len(smallDf)))
print("rows in large file: " + str(len(largeDf)))

# Take set of names from both files and check intersection to ensure no double counting
setSmallNames = set(smallDf['fileName'].tolist())
setLargeNames = set(largeDf['fileName'].tolist())
setIntersection = setLargeNames.intersection(setSmallNames)
print("fileName set intersection: " + str(setIntersection))


# Rename text columns for consistency
smallDf.rename(columns={'inBetweenText ': 'argument', 'englbetween ': 'englargument', 'documents ': 'decision', 'engldecis ': 'engldecision', 'complaint ': 'complaint', 'englcomplaint ': 'englcomplaint'}, inplace=True)
largeDf.rename(columns={'inBetweenText ': 'argument', 'englargu ': 'englargument', 'documents ': 'decision', 'engldecis ': 'engldecision', 'complaint ': 'complaint', 'englcomplaint ': 'englcomplaint'}, inplace=True)

# Add binary variable that indicates source of data
smallDf['dataSource'] = 'small'
largeDf['dataSource'] = 'large'

# Append smallDf to Large, drop Unamed Col, Add rowNumber col, write to csv
totalDf = largeDf.append(smallDf)
totalDf.drop(columns=['Unnamed: 0'], inplace=True)
totalDf['rowNumber'] = np.arange(len(totalDf))
print("rows in total file: " + str(len(totalDf)))

totalDf.to_csv('/nobackup4/murrell/dataPrepFinal/finalDataSets/CompleteData.csv', encoding='utf-8', index=False)


