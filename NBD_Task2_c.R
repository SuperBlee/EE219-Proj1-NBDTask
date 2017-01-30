#################################################################
##  EE219 Network-Backup-Dataset.
##  Task 2-c. Playing with Neural Network Prediction
##  
##  Zeyu Li
##  Jan 29, 2017
##
#################################################################

library(nnet)
library(cvTools)

dataset = read.csv("data.csv")

nor = max(dataset$Size_of_Backup) - min(dataset$Backup_Time)

bound <- floor((nrow(dataset)/10)*9)
df <- dataset[1:bound,]


# scale inputs: divide by 50 to get 0-1 range
nnet.fit <- nnet(df$Size_of_Backup/nor ~ + df$Day_of_Week + 
                   df$Hour_of_Day + df$Work_Flow_ID + 
                   df$File_Name + df$Backup_Time, 
                 data=dataset, size=20) 

df <- dataset[(bound+1):nrow(dataset),]
# multiply 50 to restore original scale
nnet_predict <- predict(nnet.fit, newdata = df)* nor 

mean((nnet_predict - df$Size_of_Backup)^2) 

plot(df$Size_of_Backup, nnet_predict, ylim = c(0, 0.01),
     main="Neural network predictions vs actual",
     xlab="Actual")
