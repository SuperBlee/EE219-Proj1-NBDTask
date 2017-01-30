#################################################################
##  EE219 Network-Backup-Dataset.
##  Task 2-a. Computing P-value with linear regression.
##  
##  Zeyu Li
##  Jan 23, 2017
##
##  * Package "DAAG and "cvTools" are required.
##  * Modifying the attribute names of the "data.csv" is also 
##      required since R cannot recognize space.
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

# Re-write the formula so that it doesn't encounter # of feature problems
train_formula <- df$Size_of_Backup ~ 
  df$WeekNum + factor(df$Day_of_Week) + 
  df$Hour_of_Day +factor(df$Work_Flow_ID) + 
  factor(df$File_Name) + df$Backup_Time

# Initialize an empty rmse list
rmse_list <- c()
pvalue_sum <- rep(0, 39)

# Vectors to record Fitted values, Fitted residuals, and Actual values
fitted_value_list <- c()
fitted_resid_list <- c()
actual_value_list <- c()

for(i in 1:k){
  # Set training set and validation set
  # train <- dataset[folds$subsets[folds$which != i], ] 
  # validation <- dataset[folds$subsets[folds$which == i], ]
  
  # Fit training data into "df"
  df <- dataset[folds$subsets[folds$which != i], ] 
  newlm <- lm(data = df, formula = train_formula)
  # Modify the "NA" in coefficients to 0.00
  newlm$coefficients[is.na(newlm$coefficients)] <- 0.00000000
  
  # Compute the RSME, append to list "rmse_list"
  smry_lm <- summary(newlm)
  rsdl <- smry_lm$residuals
  rmse <- sqrt(mean((rsdl^2)))
  rmse_list <- c(rmse_list, rmse)
  
  # Take the P-Values
  pvalue <- coef(smry_lm)[,4]
  pvalue_sum <- pvalue + pvalue_sum
  
  # Get Prediction
  df <- dataset[folds$subsets[folds$which == i], ]
  newpred <- predict(newlm,  newdata=df)
  # Get predicted residuals and actual values
  pred_residuals <- newpred - df$Size_of_Backup
  actual_value <- df$Size_of_Backup
  
  # Add data to Lists
  fitted_value_list <- c(fitted_value_list, newpred)
  fitted_resid_list <- c(fitted_resid_list, pred_residuals)
  actual_value_list <- c(actual_value_list, actual_value) 
}

# Compute the mean p-value of different attributes
pvalue_sum <- pvalue_sum / 10

# Print results we need
pvalue_sum
rmse_list

# Plotting the images and save
png(filename = "predicted_residual_vs_actual_value.png")
plot(fitted_resid_list, actual_value_list, 
     main = "Predicted Residuals v.s. Actual Value",
     xlab = "Predicted Residuals", ylab = "Actual Value")
dev.off()

png(filename = "predicted_value_vs_predicted_residuals.png")
plot(fitted_value_list, fitted_resid_list, 
     main="Predicted Value v.s. Predicted Residuals",
     xlab = "Predicted Value", ylab = "Predicted Residuals")
dev.off()

##
# From the distribution of the p-value we found that some attributes have 
# small p-values which means it closely related to the target value. 
# Hence we define another linear_model to see how it works under the same 
# setting: cross-validation.
##

train_formula_2 <- dataset$Size_of_Backup ~ 
                    factor(dataset$Day_of_Week) + dataset$Hour_of_Day +
                    factor(dataset$Work_Flow_ID) + dataset$Backup_Time

lm_2 <- lm(data = dataset, formula = train_formula_2)

plot(lm_2)



