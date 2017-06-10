#Michal Lyskawinski
#5/9/2017
######Upload data######
setwd("C:/Users/Class2017/Desktop/University/FE630")
sigma <- read.csv("sigma.csv")
sigma <- as.data.frame(as.matrix(sigma))
sigma$X <- NULL
sigma <- subset(sigma, !is.na(aa))
sigma <- lapply(sigma, function(x) type.convert(as.character(x)))
sigma <- lapply(sigma, function(x) as.numeric(x))
sigma <- as.matrix(sigma)
weights <- read.csv("weights.csv")
weights <- as.data.frame(weights)
weights <- lapply(weights, function(x) type.convert(as.character(x)))
weights <- lapply(weights, function(x) as.numeric(x))
weights <- as.matrix(weights$Market)
equlibrium <- function
(risk.aver,     # Risk Aversion
  sigma,        # Covariance matrix
  cap.weight,   # Market Cap Weights
  risk.free # Risk Free Rate
)
{
  return( risk.aver * sigma %*% cap.weight*100 +  risk.free)    
}
rf <- 5 
risk.aversion <- 2.25
impleq <- equlibrium(risk.aversion,sigma,weights,rf)
P<- read.csv("p-matrix.csv")

P <- as.matrix(P)

pmat = sum(P %*% sigma %*% t(P))
CF = pmat/(1/0.5)
omega = diag(c((1/.5)*CF,(1/.65)*CF,(1/.30)*CF))
omegaAV <- mean(c((1/.5)*CF,(1/.65)*CF,(1/.30)*CF))
tau <- pmat/omegaAV
Q<-c(10,3,1.5)

bl.compute <- function
(
  mu,         # Equilibrium returns
  cov,        # Covariance matrix
  pmat,  # Views pick matrix
  qmat,  # Views mean vector
  tau,# Measure of uncertainty of the prior estimate of the mean returns
  omega
)
{
  out = list()    
  
  temp = solve(solve(tau * cov) + t(pmat) %*% solve(omega) %*% pmat)  
  out$cov = cov + temp
  
  out$expected.return = temp %*% (solve(tau * cov) %*% mu + t(pmat) %*% solve(omega) %*% qmat)
  return(out)
}


###### COMPUTATION OF BLACK_LITTERMAN FOR THE DATA
bl.compute.posterior(impleq,sigma,P,Q,tau,omega)





