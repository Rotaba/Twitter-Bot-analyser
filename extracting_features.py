from datetime import datetime
import csv

with open('/Users/myriameayman/Documents/GUC/SaarlandMasters/Semester 2/Privacy/election-day-tweets/election_day_tweets.csv','r') as csvinput:
    with open('/Users/myriameayman/Documents/GUC/SaarlandMasters/Semester 2/Privacy/election-day-tweets/election_day_tweets_output.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('created_str')
        row.append('hashtags')
        row.append('mentions')
        all.append(row)

        for row in reader:
        	convdate = row[1]
        	a = datetime.strptime(convdate, "%Y-%m-%d %H:%M:%S")
        	b = datetime(1970, 1, 1)
        	row.append(int((a-b).total_seconds())*1000)

        	text = row[0]
        	text_arr = text.split()
        	hashtags = []
        	mentions = 0
        	for word in text_arr: 
        		if word[0]=='#':
        			hashtag = word.split('.')
        			hashtag_cleaned = hashtag[0][1:]
        			hashtag_cleaned_arr = hashtag_cleaned.encode('string-escape').split("\\x")
        			#hashtag_cleaned_arr = hashtag_cleaned.split('\\')
        			hashtags.append(hashtag_cleaned_arr[0])
        		elif word[0] == '@':
        			mentions = mentions + 1
        	row.append(hashtags)
        	row.append(mentions)		
        	all.append(row)

        writer.writerows(all)

