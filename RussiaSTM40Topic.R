datapath = "/Users/rohitk/Documents/RstmFiles/"
setwd(datapath)
getwd()
library(stm)

#Russian Descison
#prefix = "RD"

#English Descision
#prefix = "ED"

#Russian Complaint
#prefix = "RC"

#English Complaint
#prefix = "EC"

#Russian Argument(Old: Between)
#prefix = "RA"

#English Argument(Old: Between)
prefix = "EA"


# Load data based on column prefix
load(file = file.path(datapath,paste(prefix,"ProcessedVocab.rda",sep="")))

#K=40
STM40<-stm(out$documents, out$vocab,K=40, prevalence =~ s(year) + region + ruble + euro + dollar + money, data = out$meta, interactions = FALSE, init.type = "Spectral")
labelTopics(STM40, n=30, frexweight=0.25)

saveRDS(STM40,file.path(datapath,paste(prefix,"STM40Topics.rds",sep="")))

sink(file.path(datapath,paste(prefix,"STM40TopicList.txt",sep="")))
labelTopics(STM40, n=30, frexweight=0.25)
sink()
