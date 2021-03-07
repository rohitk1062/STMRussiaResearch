##### code for processing texts and then accessing the processed texts
datapath = "/Users/rohitk/Documents/RstmFiles/"
setwd(datapath)
getwd()
library(stm)

# reading data
data<-read.csv("/Users/rohitk/Documents/RstmFiles/StemmedAllText.csv")

#Russian Descison
#prefix = "RD"
#data$documents

#English Descision
#prefix = "ED"
#data$engldecis

#Russian Complaint
#prefix = "RC"
#data$complaint

#English Complaint
#prefix = "EC"
#data$englcomplaint

#Russian Argument(Old: Between)
#prefix = "RA"
#data$inBetweenText

#English Arguemnt(Old: Between)
prefix = "EA"
#data$englbetween


# reading data
data<-read.csv("/Users/rohitk/Documents/RstmFiles/StemmedAllText.csv")


# For textProcessor Need to toggle language= russian depending on col chosen
processed<-textProcessor(data$englbetween, metadata = data)
out<-prepDocuments(processed$documents, processed$vocab, processed$meta)
save(out, file = file.path(datapath,paste(prefix,"ProcessedVocab.rda",sep="")))


# can then read in the processed files at any time.
# only need the preliminaries above
load(file = file.path(datapath,paste(prefix,"ProcessedVocab.rda",sep="")))


#this is just test code to make sure that this works.
#notice the "max.em.its = 2" in the stm command, which is there simply
#to not wait for many iterations while checking it works. and also only 10 topics
STMTest<-stm(out$documents, out$vocab,K=10, prevalence =~ s(year) + region + ruble + euro + dollar + money, data = out$meta, interactions = FALSE, init.type = "Spectral",max.em.its = 2)
labelTopics(STMTest, n=30, frexweight=0.25)
