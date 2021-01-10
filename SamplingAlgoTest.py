# -*- coding: utf-8 -*-
import os
import numpy as np
import pandas as pd
import csv

PATH7 = "/nobackup4/murrell/newDataSep10"
#Previous Run
df = pd.read_csv("/nobackup4/murrell/DbData/3000SampleOct9.csv")
filenames = (list(df['fileName']))
pr = 0.018

#This function defines some basic sampling rules for the database(linear spline)
def sampleRules(num,pr):    
    if(num <= 40):
        return 0
    elif (40 < num <= 200):
        return (num)
    elif(200 < num <= 500):
        return 40 + pr*(num)
    elif(500 < num <= 1000):
        return 40 + pr*(300) + (pr/2)*(num)
    elif(1000 < num <= 10000):
        return 40 + pr*(300) + (pr/2)*(500) + (pr/4)*(num)
    elif(10000 <= num < 50000):
        return 40 + pr*(300) + (pr/2)*(500) + (pr/4)*(9000)+(pr/8)*(num)
    else:
        return 40 + pr*(300) + (pr/2)*(500) + (pr/4)*(9000)+(pr/8)*(40000)



#This function will return a list with the total sample of files.
def sampling(PATH7,seed,prob):
    totalSample = []
    
    for dirpath, dirnames, filenames in os.walk(PATH7):
        if(len(dirnames) == 0):
            np.random.seed(seed)
            if(len(filenames) != 0):
                random_files = np.random.choice(filenames, int(sampleRules(len(filenames),prob)), replace = False)
                totalSample.extend(random_files)
    return totalSample


x = sampling(PATH7,15,pr)

sampleNoDuplicate = list(set(x) - set(filenames))
print(len(sampleNoDuplicate))
print(len(x) - len(sampleNoDuplicate))
print(set(sampleNoDuplicate).intersection(set(filenames)))






