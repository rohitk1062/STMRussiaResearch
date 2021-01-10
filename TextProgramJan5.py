# -*- coding: utf-8 -*-
import os
import csv
import re
from bs4  import BeautifulSoup
import numpy as np
import pandas as pd

#Notes on Paths:
#PATH5 is the path in which all the plain text files will be of all the files that produced a failure
#PATH6 is the path where the csv files are that contain the data on the databases
#PATH7 is the path where the DB will be with only the решение cases

#Cluster Test Paths:
PATH5 = "/nobackup4/murrell/RussiaTextFails"
PATH6 = "/nobackup4/murrell/DbData"
PATH7 = "/nobackup4/murrell/newDataSep10"
PreviousRun = "/nobackup4/murrell/DbData/3000SampleOct9.csv"


#IMPORTANT: Change Pr sample parameter here Also see next few lines for pr values and number of files sampled from previous runs
#pr = 0.01, total files sampled = 14774
#pr  = 0.1, total files sampled = 47308
#pr  = 0.06, total files sampled = 38542
#pr = 0, total files sampled = 10109
#pr = 0.018 total files sampled = 18567 (17799 after deleting duplicates from Oct. 9 run)

pr = 0.018
RunName = "18kSampleJan5.csv"

#This function will create the database with the file name and path. This will print print out an excel sheet.
def filedetailDB(PATH7):
    names = []
    paths = []
    
    #List of all regions in new database
    totalRegionList = os.listdir(PATH7)
    
    for regions in totalRegionList:
        if('as-' in regions):
            regionPath1 = os.path.join(PATH7,regions)
            yearsInRegionList = os.listdir(regionPath1)
            
            for years in yearsInRegionList:
                if('.DS' not in years):
                    yearsPath1 = os.path.join(regionPath1,years)
                    filesInYearRegionCombo = os.listdir(yearsPath1)
                    
                    for files in filesInYearRegionCombo:
                        #makes sure files are xml
                        if('.xml' in files):
                            tempPath = os.path.join(yearsPath1,files)
                            
                            if('\\' in tempPath):
                                cleanPath = re.sub(r'\\','/',tempPath)
                                paths.append(cleanPath)
                                names.append(files)
                            else:
                                paths.append(tempPath)
                                names.append(files)
    
    colOrder = ['Filenames','Paths']
    dbDict = {'Filenames': names, 'Paths': paths}
    df = pd.DataFrame(dbDict)
    outputPath = os.path.join(PATH6,"filenameAndPath" + RunName)
    df[colOrder].to_csv(outputPath,index = False)
    
    fileDetailMatrix = [names,paths]
    return fileDetailMatrix
  
#This function will create the year and region database. 
#It will create an excel sheet with 3 columns:region, year, and number of cases in the year region combination 
def yearRegionDB(PATH7):
    regions = []
    years = []
    numFiles = []
    numSampled = []
    percentSampled = []
    
    for dirpath, dirnames, filenames in os.walk(PATH7):
        if(len(dirnames) == 0):
            #Added copies to fix the possibility of altering the paths themselves
            tempPath = PATH7
            tempdirPath = dirpath
            goodpath = re.sub(r'\\','/',tempPath)
            gooddirpath = re.sub(r'\\','/',tempdirPath)
            x = gooddirpath.replace(goodpath + "/",'')
            regionYear = x.split('/')
            
            #region:
            regions.append(regionYear[0])
            #year:
            years.append(regionYear[1])
            #num files in region-year combo
            numFiles.append(len(filenames))
            #number of files sampled
            numSampled.append((1/3)*int(sampleRules(len(filenames),pr)))
            #percent of files sampled
            if len(filenames) != 0:
                percentSampled.append((1/3)*int(sampleRules(len(filenames),pr)) / len(filenames))
            else:
                percentSampled.append(0)
    
    colOrder = ['Regions','Years','Number of Files','Number of Sampled Files', 'Percent of Sampled Files']        
    dbDict = {'Regions': regions, 'Years': years, 'Number of Files': numFiles, 'Number of Sampled Files': numSampled, 'Percent of Sampled Files': percentSampled}
    df = pd.DataFrame(dbDict)
    outputPath = os.path.join(PATH6,"YearAndRegion" + RunName)
    df[colOrder].to_csv(outputPath,index = False)
    fileDetailMatrix = [regions,years,numFiles]
    
    return fileDetailMatrix



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

#This function will return a list with the total sample of files.
def samplingNoDuplicate(PATH7,seed,prob):
    #Previous Run Info
    df = pd.read_csv(PreviousRun)
    prevFiles = (list(df['fileName']))
    
    totalSample = []
    for dirpath, dirnames, filenames in os.walk(PATH7):
        if(len(dirnames) == 0):
            np.random.seed(seed)
            if(len(filenames) != 0):
                random_files = np.random.choice(filenames, int(sampleRules(len(filenames),prob)), replace = False)
                totalSample.extend(random_files)
    
    #gets rid of all files from previous run in new sample. Returns as list
    return list(set(totalSample) - set(prevFiles))
    
#This is the function that will search for specified phrases and words
def csvFileWithText(sample,PATH6,filename,fileDetailDB):
    f1 = os.path.join(PATH6, filename)
    f3 = os.path.join(PATH6,"failures"+filename)
    fails = open(f3,"w+",encoding = 'utf-8',newline='')
    results = open(f1,"w+",encoding = 'utf-8',newline='')
    namesSmall1 = ['fileName','documents','region','year','ct395','ct333','absence','recall','330','ruble','euro','dollar','money','fees','accelerated','supreme','caseNumber','complaint','inBetweenText']
    namesSmall2 = ['fileName','region','year','regionFail','yearFail','caseNumberFail','decisionFail','complaintFail','inBetweenFail','isBlank','encodingError']
    dwData = csv.DictWriter(results,namesSmall1)
    failData = csv.DictWriter(fails,namesSmall2)


    cntNoDecision = 0
    cntNoComplaint = 0
    cntBlank = 0
    cntCaseNumError = 0
    cntEncodingError = 0
    cntTotalFiles = 0
    cntFailFiles = 0
    cntInBetweenError = 0
    cntRegionError = 0
    totalCharInAllFiles = 0
    
    dwData.writeheader()
    failData.writeheader()
    
    #Goes through each filename collected in the sample function
    for singleFile in sample:
        if(singleFile in fileDetailDB[0]):
            index = fileDetailDB[0].index(singleFile)
            f2 = fileDetailDB[1][index]
            cntTotalFiles += 1
        else:
            continue
                
        #Opens each .xml file and uses passes it through Beautiful soup constructor
        with open(f2, 'r', encoding = 'utf-8') as fp:
            soup = BeautifulSoup(fp,'lxml')
                
        #Dictonary with all the categories to extract information from
        Dict1 = {'fileName':'','documents':'','region':'','year':'','ct395':'','ct333':'','absence':'','recall':'','330':'','ruble':'','euro':'','dollar':'','money':'','fees':'','accelerated':'','supreme':'','caseNumber':'','complaint':'','inBetweenText':''}
        Dict2 = {'fileName':'','region':'','year':'','regionFail':'','yearFail':'','caseNumberFail':'','decisionFail':'','complaintFail':'','inBetweenFail':'','isBlank':'','encodingError':''}
        
        #Essentially T/F variables for each file that tell whether they have the following errors. Used to check file fails.
        noDecision = 0
        noComplaint = 0
        noEncoding = 0
        noCaseNum = 0
        noInBetween = 0
        noRegion = 0
        
        s = soup.get_text()
        
        s = re.sub('Ñ\s*[\ó\Ó]\s*[\ä\Ä]\s*[\ü\Ü]\s*ÿ*','Судья',s)
        s = re.sub('Ð\s*Å\s*Ø\s*È\s*Ë\s*\:*','РЕШИЛ:',s)
        s = re.sub('Î\s*Ï\s*Ð\s*Å\s*Ä\s*Å\s*Ë\s*È\s*Ë\s*\:*','ОПРЕДЕЛИЛ:',s)    
        s = re.sub('№','номер ',s)
        s = re.sub('«','\"',s)
        s = re.sub('»','\"',s)
        s = re.sub('[http]{4}s?:\/?\/?.*[\s|\r\n]','',s)
        s = re.sub('www.*[\s|\r\n]','',s)
        
        

        try:
            Dict1['region'] = soup.region.string
            Dict2['region'] = soup.region.string
            Dict2['regionFail'] = '0'
        except:
            Dict1['region'] = ''
            Dict2['region'] = ''
            Dict2['regionFail'] = '1'
            noRegion += 1
            cntRegionError += 1
        Dict1['fileName'] = singleFile
        
        try:
            dateString = soup.date.string
            yr = re.findall('\d{4}',dateString)
            Dict1['year'] = yr[0]
            Dict2['year'] = yr[0]
        except:
            Dict1['year'] = ''
            Dict2['year'] = ''
            Dict2['yearFail'] = '1'

        
        codecnt = 0
        checkEng = False
        highCount = 40 
        engPercent = 0.05
        lengthfile = len(s)
        totalCharInAllFiles += lengthfile
        
        for chars in s:
            if((1024 <= ord(chars) <= 1327) or (8 <= ord(chars) <= 13) or (32 <= ord(chars) <= 64) or (123 <= ord(chars) <= 191) or (91 <= ord(chars) <= 96) or (123 <= ord(chars) <= 126) or (ord(chars) == 8470) or (ord(chars) == 8211)):
                codecnt += 0
            else:
                codecnt += 1
        
        if(codecnt > highCount):
            checkEng = True
                
        if(checkEng == True):
            engCnt = 0
            for chars in s:
                if((65 <= ord(chars) <= 90) or (97 <= ord(chars) <= 122)):
                    engCnt += 1
            
            #Number of english characters is less than 1% of all chars in text
            if( (engCnt < int(engPercent*lengthfile)) and (codecnt - engCnt <= highCount) ):
                Dict2['encodingError'] = '0'    
            else:
                Dict2['fileName'] = singleFile
                Dict2['encodingError'] = '1'
                noEncoding += 1
                cntEncodingError += 1
        else:
            Dict2['encodingError'] = '0'         

        try:
            caseNum = soup.CaseNumber
            Dict1['caseNumber'] = caseNum
        except:
            try:
                caseNum = re.findall('А\d+-\d+/\d+',s)
                Dict1['caseNumber'] = caseNum[0]
            except:
                Dict1['caseNumber'] = ''
                Dict2['caseNumberFail'] = 'NO CASE NUMBER FOUND'
                Dict2['fileName'] = singleFile
                noCaseNum += 1
                cntCaseNumError += 1
                
            
        #Code to find complaint
        try:
            c = None
            maxLength = 100000
            complaints1 = re.findall('(?=([\А\а][\Р\р][\Б\б][\И\и][\Т\т][\Р\р][\А\а][\Ж\ж][\Н\н]*[Ы\ы]*[\Й\й]*[\Н\н]*[\О\о]*[\Г\г]*[\О\о]*\s+[\С\с][\У\у][\Д\д][\А\а]*([\s\S]*?)[\У\у]\s*[\С\с]\s*[\Т\т]\s*[\А\а]\s*[\Н\н]\s*[\О\о]\s*[\В\в]\s*[\И\и]\s*[\Л\л]\s*\:*))',s)
            #The regex search below is new. This is needed to check for complaints if the 1st search does not work.
            complaints2 = re.findall('(?=([\А\а][\Р\р][\Б\б][\И\и][\Т\т][\Р\р][\А\а][\Ж\ж][\Н\н]*[Ы\ы]*[\Й\й]*[\Н\н]*[\О\о]*[\Г\г]*[\О\о]*\s+[\С\с][\У\у][\Д\д][\А\а]*([\s\S]*?)[\И\и] приложенные*м*и*))',s)
            if(len(complaints1)== 0):
                #This is the result of the second search if the first one fails. It is in a try except so if this throws an error it goes into the except loop.
                c = complaints2[0][1]
                
                if((c is not None) and (len(c) < maxLength)):
                    z2 = ' '.join(c.split())
                    Dict1['complaint'] = z2
                else:
                    raise Exception('No complaint found')
            else:
                for i in range(len(complaints1)):
                    if (re.search('\Р\s*\Е\s*\Ш\s*\Е\s*\Н\s*\И\s*\Е',complaints1[i][1]) is None):
                        c = complaints1[i][1]
                        break
                    else:
                        c = None
                
                if((c is not None)):
                    z2 = ' '.join(c.split())
                    if(len(z2) < maxLength):
                        Dict1['complaint'] = z2
                    else:
                        raise Exception('No complaint found')
                else:
                    raise Exception('No complaint found')
                
        except:
            #Code to see if other complaint is in the file if the normal searches fail
            try:
                otherComplaint = re.findall('[\П\п][\р\Р][\и\И] [\в\В][\е\Е][\д\Д][\е\Е][\н\Н][\и\И][\и\И] [\п\П][\р\Р][\о\О][\т\Т][\о\О][\к\К][\о\О][\л\Л][\а\А]([\s\S]*?)[\У\у]\s*[\С\с]\s*[\Т\т]\s*[\А\а]\s*[\Н\н]\s*[\О\о]\s*[\В\в]\s*[\И\и]\s*[\Л\л]\s*\:*',s)
                if(len(otherComplaint) == 1):
                    c = otherComplaint[0][1]
                    
                    if((c is not None) and (len(c) < maxLength)):
                        z2 = ' '.join(c.split())
                        Dict1['complaint'] = z2
                    else:
                        raise Exception('No complaint found')
                else:
                    raise Exception('No complaint found')
            except:
                cntNoComplaint += 1
                noComplaint += 1
                Dict2['fileName'] = singleFile
                Dict1['complaint'] = ''
                Dict2['complaintFail'] = 'COMPLAINT NOT FOUND'
                
                
        
        #Code to get Decision
        try:
            short = 100000
            x = None
            decisions1 = re.findall('[\Р\р]\s*[\Е\е]\s*[\Ш\ш]\s*[\И\и]\s*[\Л\л]\s*\:*([\s\S]*?)[\С\с]\s*[\У\у]\s*[\д\Д]\s*[\ь\Ь]\s*[\И\и]*[\я\Я]*\s*\:*',s)
            decisions2 = re.findall('[\Р\р]\s*[\Е\е]\s*[\Ш\ш]\s*[\И\и]\s*[\Л\л]\s*\:*([\s\S]*?)[\П\п]\s*[\р\Р]\s*[\е\Е]\s*[\д\Д]\s*[\с\С]\s*[\е\Е]\s*[\д\Д]\s*[\а\А]\s*[\т\Т]\s*[\е\Е]\s*[\л\Л]\s*[\ь\Ь]',s)
            decisions3 = re.findall('[\Р\р]\s*[\Е\е]\s*[\Ш\ш]\s*[\И\и]\s*[\Л\л]\s*\:([\s\S]*?)[\С\с]\s*[\У\у]\s*[\д\Д]\s*[\ь\Ь]\s*[\И\и]*[\я\Я]*\s*\:*',s)
            
            if len(decisions3) != 0:
                for things in decisions3:
                    if((len(things) < short)and len(things) != 0):
                        x = things
                        short = len(things)
                
                if (x is not None):
                    s2 = ' '.join(x.split())
                    Dict1['documents'] = s2
                else:
                    raise Exception('No decision found')
            
            elif(len(decisions1) != 0):
                for things in decisions1:
                    if((len(things) < short)and len(things) != 0):
                        x = things
                        short = len(things)
                
                if (x is not None):
                    s2 = ' '.join(x.split())
                    Dict1['documents'] = s2
                else:
                    raise Exception('No decision found')
            
            else:
                for things in decisions2:
                    if((len(things) < short)and len(things) != 0):
                        x = things
                        short = len(things)
            
                if (x is not None):
                    s2 = ' '.join(x.split())
                    Dict1['documents'] = s2
                else:
                    raise Exception('No decision found')
            
        except:
            cntNoDecision += 1
            noDecision += 1
            Dict2['fileName'] = singleFile
            Dict1['documents']=''
            Dict2['decisionFail']= 'DECISION NOT FOUND'
            
        
        
        
        #Code to find in between text
        try:
            if(noDecision == 0 and noComplaint == 0):
                r1 = re.findall('[\У\у]\s*[\С\с]\s*[\Т\т]\s*[\А\а]\s*[\Н\н]\s*[\О\о]\s*[\В\в]\s*[\И\и]\s*[\Л\л]\s*\:*([\s\S]*?)[\Р\р]\s*[\Е\е]\s*[\Ш\ш]\s*[\И\и]\s*[\Л\л]\s*\:*',s)
                r2 = re.findall('[\И\и] приложенные?м?и?([\s\S]*?)[\Р\р]\s*[\Е\е]\s*[\Ш\ш]\s*[\И\и]\s*[\Л\л]\s*\:*',s)
                
                if(r1 is None):
                    textInBetween = r2
                else:
                    textInBetween = r1
                
                for text in textInBetween:
                    if(len(text) > 20):
                        s3 = ' '.join(text.split())
                        Dict1['inBetweenText'] = s3
                        break
                    else:
                        raise Exception('inBetweenFail')
        except:
            Dict2['fileName'] = singleFile
            Dict1['inBetweenText']=''
            Dict2['inBetweenFail']= 'FAIL'
            cntInBetweenError += 1
            noInBetween += 1
            
            
            
        
        
        #Code to Search for CT395
        ct1 = re.search('ст.\s*395',s)
        ct2 = re.search('стат.\s*395',s)
        ct3 = re.search('стат[\u0410-\u044F]+\s*395',s)
            
        if (ct1 is not None or ct2 is not None or ct3 is not None):
            Dict1['ct395'] = '1'
        else:
            Dict1['ct395'] = '0'
        
        #Code to Search for CT333
        ct4 = re.search('ст.\s*333',s)
        ct5 = re.search('стат.\s*333',s)
        ct6 = re.search('стат[\u0410-\u044F]+\s*333',s)
            
        if (ct4 is not None or ct5 is not None or ct6 is not None):
            Dict1['ct333'] = '1'
        else:
            Dict1['ct333'] = '0'
        
        
        #Code to search for в отсутствие(in absence of)
        absence = re.search('в отсутствие',s)
        
        if(absence is not None):
            Dict1['absence'] = '1'
        else:
            Dict1['absence'] = '0'
        
        
        
        #Code to search for в отзыве(in recall)
        recall = re.search('в отзыве',s)
        
        if(recall is not None):
            Dict1['recall'] = '1'
        else:
            Dict1['recall'] = '0'
            
        #Code to search for Ct.330
        para = re.findall('[\Р\р]уководствуясь([\s\S]*?)[\Р\р]\s*[\Е\е]\s*[\Ш\ш]\s*[\И\и]\s*[\Л\л]\s*\:*',s)
        if(para is not None):
            try:
                if(re.search('330',para[0]) is not None):
                    Dict1['330'] = '1'
                else:
                    ct1 = re.search('ст.\s*330',s)
                    ct2 = re.search('стат.\s*330',s)
                    ct3 = re.search('стат[\u0410-\u044F]+\s*330',s)
                
                    if (ct1 is not None or ct2 is not None or ct3 is not None):
                        Dict1['330'] = '1'
                    else:
                        Dict1['330'] = '0'
            except:
                ct1 = re.search('ст.\s*330',s)
                ct2 = re.search('стат.\s*330',s)
                ct3 = re.search('стат[\u0410-\u044F]+\s*330',s)
            
                if (ct1 is not None or ct2 is not None or ct3 is not None):
                    Dict1['330'] = '1'
                else:
                    Dict1['330'] = '0'
        else:
            ct1 = re.search('ст.\s*330',s)
            ct2 = re.search('стат.\s*330',s)
            ct3 = re.search('стат[\u0410-\u044F]+\s*330',s)
            
            if (ct1 is not None or ct2 is not None or ct3 is not None):
                Dict1['330'] = '1'
            else:
                Dict1['330'] = '0'
                
        #search for rubles
        rubles = re.search('\s?[.!?\\-]?руб.[.!?\\-]?\s?',s)
        if(rubles is not None):
            Dict1['ruble'] = '1'
        else:
            Dict1['ruble'] = '0'
        
        #search for euros
        euros = re.search('(\s|[.!?\\-])евро([.!?\\-]|\s)',s)
        if(euros is not None):
            Dict1['euro'] = '1'
        else:
            Dict1['euro'] = '0'
            
        #search for dollars
        dollars = re.search('([.!?\\-]|\s)доллар[\u0410-\u044F]{1,3}\s*США([.!?\\-]|\s)',s)
        if(dollars is not None):
            Dict1['dollar'] = '1'
        else:
            Dict1['dollar'] = '0'
        
        #Search for money
        if(Dict1.get('ruble') == 1 or Dict1.get('euro') == 1 or Dict1.get('dollar') == 1):
            Dict1['money'] = '1'
        else:
            Dict1['money'] = '0'
            
        #Search for Fees:
        fee = re.search('судебн[\u0410-\u044F]{2}\s+издерж[\u0410-\u044F]{2}([.!?\\-]|\s)',s)
        if(fee is not None):
            Dict1['fees'] = '1'
        else:
            Dict1['fees'] = '0'
        
        #Search for accelerated:
        accel = re.search('упрощенн[\u0410-\u044F]{2,}([.!?\\-]|\s)',s)
        if(accel is not None):
            Dict1['accelerated'] = '1'
        else:
            Dict1['accelerated'] = '0'
        
        
        #Search for Supreme:
        supreme1 = re.search('Постановлени[\u0410-\u044F]\s+Пленума\s+Верховного([.!?\\-]|\s)',s)
        supreme2 = re.search('Постановлени[\u0410-\u044F]\s+Пленума\s+Высшего([.!?\\-]|\s)',s)
        
        if(supreme1 is not None or supreme2 is not None):
            Dict1['supreme'] = '1'
        else:
            Dict1['supreme'] = '0'
        
        
        if(noDecision == 1 and noComplaint == 1):
            Dict2['isBlank'] = '1'
            cntBlank += 1
        else:
            Dict2['isBlank'] = '0'
            
        #Writes the entire row only if there are no errors
        if(noDecision == 0 and noComplaint == 0 and noEncoding == 0 and noCaseNum == 0 and noInBetween == 0 and noRegion == 0):
            dwData.writerow(Dict1)
        else:
            #Writes text files of the files that produce errors. 
            cntFailFiles += 1
            f5 = os.path.join(PATH5, singleFile + 'fail.txt')
            textfail = open(f5,"w+",encoding = 'utf-8',newline='')
            textfail.write(s)
            textfail.close()
            failData.writerow(Dict2)
        
    #Prints numbers of blank files, files w/o complains, and files w/o decisions
    print("Number of files processed:" + str(cntTotalFiles))
    print("% of good files:" + str((cntTotalFiles - cntFailFiles)/cntTotalFiles * 100)+"%")
    print("% of fail files:" + str(cntFailFiles/cntTotalFiles * 100))
    print("% of files with no decision: " + str(cntNoDecision/cntTotalFiles * 100)+"%")
    print("% of files without complaint: " + str(cntNoComplaint/cntTotalFiles * 100)+"%")
    print("% of blank files: " + str(cntBlank/cntTotalFiles * 100)+"%")
    print("% of files with poor encoding: " + str(cntEncodingError/cntTotalFiles * 100)+"%")
    print("% of files with no case number: " + str(cntCaseNumError/cntTotalFiles * 100)+"%")
    print("% of files with the in between error(reshenie only): " + str(cntInBetweenError/cntTotalFiles * 100)+"%")
    print("% of files with no region: " + str(cntRegionError/cntTotalFiles * 100)+"%")
    print("Mean number of characters in a passed text files: " + str(totalCharInAllFiles/cntTotalFiles))

    results.close()
    fails.close()
    return

y = filedetailDB(PATH7)
yearRegionDB(PATH7)
x = samplingNoDuplicate(PATH7,15,pr)
csvFileWithText(x,PATH6,RunName,y)







        
   



