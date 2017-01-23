#################################################################
##  EE219 Network-Backup-Dataset.
##  Task 2. Computing P-value with linear regression.
##  
##  Zeyu Li
##  Jan 23, 2017
#################################################################
library(DAAG)
library(cvTools)

# Load dataset
dataset <- read.csv("data.csv")

# Create 10-fold cross validation
k <- 10
folds <- cvFolds(nrow(dataset), K=k)

train_formula <- train$Size_of_Backup ~ 
  train$WeekNum + factor(train$Day_of_Week) + 
  train$Hour_of_Day +factor(train$Work_Flow_ID) + 
  factor(train$File_Name) + train$Backup_Time

# Initialize rmse list
rmse_list <- c()

for(i in 1:k){
  # Set training set and validation set
  train <- dataset[folds$subsets[folds$which != i], ] 
  validation <- dataset[folds$subsets[folds$which == i], ]
  
  # Fit training data
  newlm <- lm(data = train, formula = train_formula)
  smry_lm <- summary(newlm)
  
  # Compute the RSME, append to list "rmse_list"
  rsdl <- smry_lm$residuals
  rmse <- sqrt(mean((rsdl^2)))
  rmse_list <- c(rmse_list, rmse)
  
  # 
  
  # Get Prediction
  newpred <- predict(newlm, newdata = validation) 
  sm_pred <- summary(newpred)
  sm_pred 
}

