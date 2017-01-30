#################################################################
##  EE219 Network-Backup-Dataset.
##  Task 2-b. Playing with Random Forest
##  
##  Zeyu Li
##  Jan 29, 2017
##
#################################################################

library("randomForest", lib.loc="~/R/win-library/3.3")

dataset <- read.csv("data.csv")

train_formula <- dataset$Size_of_Backup ~ 
  dataset$WeekNum + dataset$Day_of_Week + 
  dataset$Hour_of_Day + dataset$Work_Flow_ID + 
  dataset$File_Name + dataset$Backup_Time

{
ntree_list <- seq(20,100,20)
ns_list <- seq(4,10,2)

mse <- c()

for (ns in ns_list){
  for (nt in ntree_list){
    rf <- randomForest(train_formula, data=dataset, ntree = nt, nodesize = ns)
    print(c(ns,nt))
    m_mse <- mean(rf$mse)
    mse <- c(mse, m_mse)
  }
}

}

{
png("mse_vs_ntree.png")

plot(0,0,xlim=c(20,100),ylim=c(0,0.0007), xlab = "Number of Trees", ylab = "MSE", main = "MSE v.s. Number of Trees in Tuning Random Forest")
for(i in 1:4){
  lines(seq(20,100,20),mat_mse[i,], col=cl[i], type="b")
}
legend('topright', legend = c("4","6","8", "10"), col=cl[1:4], lty=1)

dev.off()
}

{
png("mse_vs_nodesize.png")

plot(0,0,xlim=c(4,10),ylim=c(0,0.0007), xlab = "Size of node", ylab = "MSE", main = "MSE v.s. Size of Node in Tuning Random Forest")
for(i in 1:5){
  lines(seq(4,10,2),mat_mse[,i], col=cl[i], type="b")
}
legend('topright', legend = c("20","40","60","80","100"), col=cl[1:5], lty=1)

dev.off()
}

rf <- randomForest(train_formula, data=dataset, importance = TRUE, ntree = 20)
rf$importance

# > rf$importance
# %IncMSE IncNodePurity
# dataset$WeekNum      -5.167108e-06     0.5020352
# dataset$Day_of_Week   7.935237e-03    46.8410639
# dataset$Hour_of_Day   3.964253e-03    24.2785207
# dataset$Work_Flow_ID  5.349584e-03    28.0905400
# dataset$File_Name     4.967671e-03    20.6745791
# dataset$Backup_Time   8.424219e-03    73.1862482
