library(stm)
datapath = "/nobackup4/murrell/DbData/SplitFilesForSTM/StemmedAllText.csv"

#Russian Descison
Outpath = "/nobackup4/murrell/STMTestingResults/DecisionInfo/Russian"
prefix = "RD"

#English Descision
#Outoath = "/nobackup4/murrell/STMTestingResults/DecisionInfo/English"
#prefix = "ED"

#Russian Complaint
#Outpath = "/nobackup4/murrell/STMTestingResults/ComplaintInfo/Russian"
#prefix = "RC"

#English Complaint
#Outpath = "/nobackup4/murrell/STMTestingResults/ComplaintInfo/English"
#prefix = "EC

#Russian Between
#Outpath = "/nobackup4/murrell/STMTestingResults/BetweenInfo/Russian"
#prefix = "RB"

#English Between
#Outpath = "/nobackup4/murrell/STMTestingResults/BetweenInfo/English"
#prefix = "EB"

data<-read.csv(datapath)

#Need to toggle language= russian depending on col chosen
# Also change data$documents based on col
processed <- textProcessor(data$documents, metadata = data,language="russian")

#Prep Docs
sink(file.path(Outpath,paste(prefix,"prepConsoleOut.txt",sep="")))
out <- prepDocuments(processed$documents, processed$vocab, processed$meta)
sink()
save(out,file= file.path(Outpath,paste(prefix,"OutFile.rda",sep="")))

set.seed(1)

# K Search
sink(file.path(Outpath,paste(prefix,"KSearchConsole.txt",sep="")))
KSearch <-searchK(out$documents, out$vocab, K=c(10,20,30,40,50,60,70), prevalence =~ s(year)+region,data=out$meta, interactions = FALSE, init.type = "Spectral")
sink()
saveRDS(KSearch,file.path(Outpath,paste(prefix,"KSearchObject.rds",sep="")))
pdf(file.path(Outpath,paste(prefix,"KSearchDiagnostics.pdf",sep="")))
plot.searchK(KSearch)
dev.off()

xclus<-KSearch$results$exclus
semcoh<-KSearch$results$semcoh
pdf(file.path(Outpath,paste(prefix,"XclusSemcoh.pdf",sep="")))
plot(xclus, semcoh,col="lightblue", pch=19, cex=2)
text(xclus, semcoh, labels=KSearch$results$K, cex=0.9, font=2)
dev.off()