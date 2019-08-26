library(stringi)
table <- read.csv(file="~/Documents/GUC/SaarlandMasters/Semester 2/Privacy/russian-troll-tweets/tweets.csv", header=TRUE, sep=",")
table <- table[with(table, order(table[,2],table[,3])),]
table<-table[!(is.na(table$user_id) & is.na(table$user_key)),]
table_2 <- table[ , !names(table) %in% c("user_id", "user_key", "created_str", "retweeted", "tweet_id", "source", "expanded_urls", "posted", "retweeted_status_id", "in_reply_to_status_id")]
table_2 <- data.frame(lapply(table_2, as.character), stringsAsFactors=FALSE)
empty <- array(numeric(),c(203482,7))

print(stri_sub(table[1,2], 1,-1) == "_billy_moyer_")
print(stri_sub(table[1,2], 1,-1))
row <- 1
while (row <= nrow(table)) {
  curr_name <- stri_sub(table[row,2], 1,-1) # user_key
  flag = FALSE
  if (is.na(curr_name)) {
    curr_name <- table[row,1] # user_id
    flag = TRUE
  }
  curr_date <- table[row,3] # created_at
  cond = TRUE
  while (!is.na(cond) && cond) {
    empty[row,6] <- table[row,3] - curr_date # e6 = created_at
    curr_date <- table[row,3]
    row <- row + 1
    if (flag) {
      cond <-  stri_sub(table[row,1], 1,-1) == curr_name
    }
    else {
      cond <- stri_sub(table[row,2], 1,-1) == curr_name
    }
    #print(cond)
  }
  print(row)
}

#print(row)
for (row in 1:nrow(table_2)) {
  empty[row,7] <- 1
  empty[row,1] <- table_2[row,1]
  empty[row,4] <- length(as.list(strsplit(stri_sub(table_2[row, 5], 2, -2), ",")[[1]]))
  if (is.na(table_2[row,2])) {
    empty[row,2] = 0
  }
  else {
    empty[row,2] = table_2[row, 2]
  }
  if (is.na(table_2[row,3])) {
    empty[row,3] = 0
  }
  else {
    empty[row,3] = table_2[row, 3]
  }
  empty[row,5] <- length(as.list(strsplit(stri_sub(table_2[row, 6], 2, -2), ",")[[1]]))
}
write.csv(empty,file="dataset.csv")

table_elec_day <- read.csv(file="~/Documents/GUC/SaarlandMasters/Semester 2/Privacy/election-day-tweets/election_day_tweets_output.csv", header=TRUE, sep=",")
table_elec_ordered <- table_elec_day[with(table_elec_day, order(table_elec_day[,24],table_elec_day[,35])),]
table_elec_ordered<-table_elec_ordered[!(is.na(table_elec_ordered$user.id) & is.na(table_elec_ordered$user.screen_name)),]
print(colnames(table_elec_ordered))
table_elec_ordered_2 <- table_elec_ordered[ , names(table_elec_ordered) %in% c("user.id", "user.screen_name", "created_str", "id", "favorite_count","retweet_count", "mentions", "hashtags")]
table_elec_ordered_2 <- data.frame(lapply(table_elec_ordered_2, as.character), stringsAsFactors=FALSE)
cleaned_elec <- array(numeric(),c(397629,7))


row <- 1
while (row <= nrow(cleaned_elec)) {
  curr_name <- stri_sub(table_elec_ordered_2[row,2], 1,-1)
  flag = FALSE
  if (is.na(curr_name)) {
    curr_name <- table_elec_ordered_2[row,1]
    flag = TRUE
  }
  curr_date <- as.numeric(table_elec_ordered_2[row,6])
  cond = TRUE
  while (!is.na(cond) && cond) {
    cleaned_elec[row,6] <- as.numeric(table_elec_ordered_2[row,6]) - as.numeric(curr_date)
    curr_date <- as.numeric(table_elec_ordered_2[row,6])
    row <- row + 1
    if (flag) {
      cond <-  stri_sub(table_elec_ordered_2[row,1], 1,-1) == curr_name
    }
    else {
      cond <- stri_sub(table_elec_ordered_2[row,2], 1,-1) == curr_name
    }
    #print(cond)
  }
  print(row)
}

for (row in 1:nrow(cleaned_elec)) {
if (grepl(table_elec_ordered_2[row,1], table$user_id) || grepl(table_elec_ordered_2[row,2], table$user_key)){
    cleaned_elec[row,1] = 1
  }
  else {
    cleaned_elec[row,1] = 0
  }
  cleaned_elec[row,1] <- table_elec_ordered_2[row,6]
  cleaned_elec[row,4] <- length(as.list(strsplit(stri_sub(table_elec_ordered_2[row, 7], 2, -2), ",")[[1]]))
  if (is.na(table_elec_ordered_2[row,5])) {
    cleaned_elec[row,2] = 0
  }
  else {
    cleaned_elec[row,2] = table_elec_ordered_2[row, 5]
  }
  if (is.na(table_elec_ordered_2[row,4])) {
    cleaned_elec[row,3] = 0
  }
  else {
    cleaned_elec[row,3] = table_elec_ordered_2[row, 4]
  }
  #cleaned_elec[row,5] <- length(as.list(strsplit(stri_sub(table_2[row, 6], 2, -2), ",")[[1]]))
  cleaned_elec[row,5] <- table_elec_ordered_2[row, 8]
  print(row)
}
write.csv(cleaned_elec,file="~/Documents/GUC/SaarlandMasters/Semester 2/Privacy/election-day-tweets/cleaned_elec.csv")