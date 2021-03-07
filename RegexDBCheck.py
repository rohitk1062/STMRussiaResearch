# -*- coding: utf-8 -*-
import pandas as pd


metadataCols = ['fileName', 'region', 'year', 'ct395', 'ct333', 'absence', 'recall', '330', 'ruble', 'euro', 'dollar', 'money', 'fees','accelerated', 'supreme', 'caseNumber']
originalFile = "/nobackup4/murrell/RegexFiles/TranslatedDecisionComplaint18000.csv"
filteredFile = "/nobackup4/murrell/RegexFiles/FilteredTranslatedDecisionComplaint18000.csv"

#filteredFile = "/Users/rohitk/Documents/RstmFiles/TranslatedDecisionComplaintBetween3000.csv"
#originalFile = "/Users/rohitk/Documents/RstmFiles/StemmedAllText.csv"

ogDf = pd.read_csv(originalFile)
newDf = pd.read_csv(filteredFile)

# Check to see if the same number of rows
print("og row: " + str(len(ogDf)))
print("new row: " + str(len(newDf)))

# only keep metadata cols and check if dfs are equal
ogMetadata = ogDf[metadataCols]
newMetadata = newDf[metadataCols]
print("Files are equal: " + str(ogMetadata.equals(newMetadata)))

# Keep only english text cols
ogText = ogDf[['englDecision','englComplaint','englBetween']]
newText = newDf[['engldecision','englcomplaint','englbetween']]

# Loop through englihs text cols
for i in range(0, len(ogText.index)):
    for j in range(0, len(ogText.columns)):
        doc1 = str(ogText.values[i, j]).lower()
        doc2 = str(newText.values[i, j]).lower()

        lenDiff = abs(len(doc1) - len(doc2))

        # If lenDiff == 0 there are no changes since all of our changes are shortening the doc
        if lenDiff > 0:
            print("Difference in length: " + str(lenDiff))
            ogWordSet = set(doc1.split())
            newWordSet = set(doc2.split())
            diffSet = newWordSet.difference(ogWordSet)
            diffSet2 = ogWordSet.difference(newWordSet)
            print("Words in new col that are not in old: " + str(diffSet))
            print("Words in old col that are not in new: " + str(diffSet2))







