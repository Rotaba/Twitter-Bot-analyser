library(class)
library(gmodels)
require(MASS)
require(splines)
require(ISLR)
require(gam)
library(mgcv)
library("e1071")
library(pROC)
#read data and normalize it 
#Yannick's database 
table <- read.csv(file="~/Documents/GUC/SaarlandMasters/Semester2/Privacy/Pet18/3000_comb/3000_rnd_combined.csv", header=TRUE, sep=",")
table <- table[,3:108]

#Roman's database 
#table <- read.csv(file="~/Documents/GUC/SaarlandMasters/Semester2/Privacy/Pet18/3000_comb/shuf_comb3000_yesHead.csv", header=TRUE, sep=",")
#table <- table[,!colnames(table) %in% c("time_difference","X0")]
#table <- table[,2:107]

#Full dataset
table <- read.csv(file="~/Documents/GUC/SaarlandMasters/Semester2/Privacy/Pet18/data/dataset_combined.csv", header=TRUE, sep=",")
table <- table[,2:ncol(table)]

table <- table[,!colnames(table) %in% c("time_difference","X0", "retweet_count", "favorite_count","hashtags", "mentions","created_at")]
#table <- table[,!colnames(table) %in% c("time_difference","X0","created_at")]
table_norm <- as.data.frame(scale(table[,!colnames(table) %in% c("output")]))
output <- table$output
table_norm <- cbind(table_norm, output)

print("Starting leverage")
lm.model <- lm(output ~ .,data=table_norm)
hatvalues_frame <- as.data.frame(hatvalues(lm.model))
mn <-mean(hatvalues(lm.model))
hatvalues_frame$warn <- ifelse(hatvalues_frame[, 'hatvalues(lm.model)']>3*mn, 'l3',
                               ifelse(hatvalues_frame[, 'hatvalues(lm.model)']>2*mn, 'l3', '-' ))

new <- hatvalues_frame$warn
table_norm <- subset(table_norm, new!="l3")
print("Finish leverage")

size_of_train <- floor(nrow(table_norm)*0.8)
print(size_of_train)
start_of_test <- size_of_train + 1
#split into train and test data
table_norm.train <- table_norm[1:size_of_train,]
table_norm.test <- table_norm[start_of_test:nrow(table_norm),]

print("Starting KNN")
#perform KNN
#knn_pred <- knn(train = table_norm.train[,!colnames(table_norm) %in% c("output")], test = table_norm.test[,!names(table) %in% c("output")],cl = table_norm.train$output, k=10)
#knn.misClasificError <- mean(knn_pred != table_norm.test$output)
#print(paste('Accuracy in Knn: ',1 - knn.misClasificError))

print("Starting logistic regression")
#perform logistic regression
log_reg.model <- glm(output ~.,family=binomial(link='logit'),data=table_norm.train)
log_reg.pred <- predict(log_reg.model,newdata=subset(table_norm.test,select=!names(table_norm.test) %in% c("output")),type='response')
log_reg.pred <- ifelse(log_reg.pred > 0.5,1,0)
log_reg.misClasificError <- mean(log_reg.pred != table_norm.test$output)
log_reg.auc <- auc(log_reg.pred, table_norm.test$output)
print(paste('Accuracy of logistic regression: ',1-log_reg.misClasificError))
print(paste('AUC of logistic regression: ',log_reg.auc))
print("Starting lda")
#perform lda
lda_model.model <- MASS::lda(formula = output ~ ., data = table_norm.train, subset=1:2400)
lda_model.pred <- predict(lda_model.model,newdata=subset(table_norm.test,select=!names(table_norm.test) %in% c("output")),type='response')$class
lda_model.misClasificError <- mean(lda_model.pred != table_norm.test$output)
lda_model.auc <- auc(lda_model.pred, table_norm.test$output)
print(paste('Accuracy of LDA: ',1-lda_model.misClasificError))
print(paste('AUC of LDA: ',lda_model.auc))

print("Starting qda")
#perform qda
qda_model.model <- MASS::qda(formula = output ~ ., data = table_norm.train, subset=1:2400)
qda_model.pred <- predict(qda_model.model,newdata=subset(table_norm.test,select=!names(table_norm.test) %in% c("output")),type='response')$class
qda_model.misClasificError <- mean(qda_model.pred != table_norm.test$output)
qda_model.auc <- auc(qda_model.pred, table_norm.test$output)
print(paste('Accuracy of QDA: ',1-qda_model.misClasificError))
print(paste('AUC of QDA: ',qda_model.auc))

print("Starting Splines")
formula = "output ~ "
for (i in 2:ncol(table_norm)-1) {
  if (i > 1)
  formula = paste(formula, "+ s(", colnames(table_norm)[i], ", k=5)")
  else formula = paste(formula, "s(", colnames(table_norm)[i], ", k=5)")
}
#perform splines
splines_model.model <-gam(as.formula(formula), data = table_norm.train )
splines_model.pred <- predict(splines_model.model,newdata=subset(table_norm.test,select=!names(table_norm.test) %in% c("output")),type='response')
splines_model.pred <- ifelse(splines_model.pred > 0.5,1,0)
splines_model.misClasificError <- mean(splines_model.pred != table_norm.test$output)
splines_model.auc <- auc(splines_model.pred, table_norm.test$output)
print(paste('Accuracy of Splines: ',1-splines_model.misClasificError))
print(paste('AUC of Splines: ',splines_model.auc))

print("Starting SVM")
#perform SVM
svm_model.model <- svm(output ~ ., data = table_norm.train, method="C-classification",kernel="linear")
svm_model.pred <- predict(svm_model.model,subset(table_norm.test,select=!names(table_norm.test) %in% c("output")))
svm_model.pred <- ifelse(svm_model.pred > 0.5,1,0)
svm_model.auc <- auc(svm_model.pred, table_norm.test$output)
print(paste('Accuracy of SVM: ', mean(svm_model.pred==table_norm.test$output)))
print(paste('AUC of SVM: ',svm_model.auc))