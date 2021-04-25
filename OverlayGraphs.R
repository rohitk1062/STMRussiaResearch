library(stm)

EnglishSearchK <- readRDS(file = "/Users/rohitk/Documents/RstmFiles/EBKSearchObject.rds")
RussianSearchK <- readRDS(file = "/Users/rohitk/Documents/RstmFiles/RBKSearchObject.rds")
g <- EnglishSearchK$results
h <- RussianSearchK$results


pdf("/Users/rohitk/Documents/RstmFiles/OverlayDecisionDiagnostic.pdf")
oldpar <- par(no.readonly=TRUE)
par(mfrow=c(2,2),mar=c(4,4,4,4),oma=c(2,2,2,2),xpd=TRUE)

plot(g$K,g$heldout,type="p", main="Held-Out Likelihood", xlab="Number of Topics (K)", ylab="Held-Out Likelihood",ylim=range(c(h$heldout,g$heldout)))
lines(g$K,g$heldout,lty=1,col=1)
points(h$K,h$heldout,lty=1,col=2)
lines(h$K,h$heldout,lty=1,col=2)

plot(g$K,g$residual,type="p", main="Residuals", xlab="Number of Topics (K)", ylab="Residuals",ylim=range(c(h$residual,g$residual)))
lines(g$K,g$residual,lty=1,col=1 )
lines(h$K,h$residual,lty=1,col=2 )
points(h$K,h$residual,lty=1,col=2 )


plot(g$K,g$semcoh,type="p", main="Semantic Coherence", xlab="Number of Topics (K)", ylab="Semantic Coherence",ylim=range(c(h$semcoh,g$semcoh)))
lines(g$K,g$semcoh,lty=1,col=1 )
lines(h$K,h$semcoh,lty=1,col=2 ) 
points(h$K,h$semcoh,lty=1,col=2 ) 


plot(g$K,g$lbound,type="p", main="Lower Bound", xlab="Number of Topics (K)", ylab="Lower Bound",ylim=range(c(h$lbound,g$lbound)))
lines(g$K,g$lbound,lty=1,col=1 )
lines(h$K,h$lbound,lty=1,col=2 ) 
points(h$K,h$lbound,lty=1,col=2 ) 


title("Diagnostic Values by Number of Topics", outer=TRUE)

par(fig = c(0, 1, 0, 1), oma = c(0, 0, 0, 0), mar = c(0, 0, 0, 0), new = TRUE)
plot(0, 0, type = 'l', bty = 'n', xaxt = 'n', yaxt = 'n')
legend('bottom',legend = c("English", "Russian"), col = c("black","red"), lwd = 5, xpd = TRUE, horiz = TRUE, cex = 1, seg.len=1, bty = 'n')
par(oldpar)
dev.off()



pdf("/Users/rohitk/Documents/RstmFiles/XclusSemcohArgument.pdf")
plot(g$exclus, g$semcoh,pch=26, cex=2,ylim=range(c(h$semcoh,g$semcoh)),xlim=range(c(h$exclus,g$exclus)),xlab="exclusivity",ylab="semantic coherence")
text(g$exclus, g$semcoh, labels=g$K, cex=0.75, font=2,col="black")
points(h$exclus, h$semcoh,col="red", pch=26, cex=2)
text(h$exclus, h$semcoh, labels=g$K, cex=0.75, font=2,col="red")
legend('topright',legend = c("English", "Russian"), col = c("black","red"), lwd = 2, cex = 0.75,ncol= 1)
dev.off()

