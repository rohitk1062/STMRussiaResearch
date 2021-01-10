library(stm)
setwd("/Users/rohitk/Documents/RstmFiles")
data<-read.csv("StemmedTranslatedDecisionComplaintBetween3000.csv")
#Add language= "russian" if necessary
processed<-textProcessor(data$englDecision, metadata = data)
sink("PrepStemEnglishDecision.txt")
out<-prepDocuments(processed$documents, processed$vocab, processed$meta)
sink()
save(out,file="StemmedEnglishDecision.rda")

load(file = "/Users/rohitk/Documents/RstmFiles/DecisionInfo/StemmedEnglishDecision.rda")
STM10<-stm(out$documents, out$vocab, K=10, prevalence =~ s(year)+region ,data = out$meta, interactions = FALSE, init.type = "Spectral", max.em.its=2)
sink("EnglishDecisionTopics.txt")
labelTopics(STM10, n=30, frexweight=0.25)
sink()
saveRDS(STM10, file="StemmedEnglishDecisionSTMRes.rds")

#START OF SEARCH K PROGRAM

load(file = "StemmedRussianDecision.rda")
set.seed(1)

STM10 <- readRDS(file = "StemmedEnglishDecisionSTMRes.rds")

#saves console output to file
K3000Search <-searchK(out$documents, out$vocab, K=c(10,20,30), prevalence =~ s(year)+region,data=out$meta, interactions = FALSE, init.type = "Spectral")
saveRDS(K3000Search,"KSearchRussianDecision.rds")
K3000Search
pdf("K3000RussianDecision.pdf")
plot.searchK(K3000Search)
dev.off()

setwd("/Users/rohitk/Documents/RstmFiles/DecisionInfo")
K3000Search <- readRDS(file = "KSearchRussianDecision.rds")
#extract exclus and semcoh
xclus<-K3000Search$results$exclus
semcoh<-K3000Search$results$semcoh
pdf("XclusSemcohRussianDecision.pdf")
plot(xclus, semcoh,col="lightblue", pch=19, cex=2)
text(xclus, semcoh, labels=K3000Search$results$K, cex=0.9, font=2)
dev.off()



#Document topic proportions
#plot(STM10,type="hist")

#fix sizing for labels plot
#plot(R16,type="labels",text.cex = 0.60)

#top topics
#plot(R16,type="summary")

#compare words in 2 topics
#plot(R16,type="perspectives", topics=c(3,2))

#graph with correlation network
#Rcorr <- topicCorr(R16)
#plot(Rcorr, vertex.color ="black", vertex.label.cex = 0.7, vertex.label.color = "white")


