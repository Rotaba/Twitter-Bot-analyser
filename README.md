## Paper
See PDF in repo or 
https://www.sharelatex.com/6679699354fdqvmrgbtkrw

## Workflow

train test epochs: `./05-evaluate.py ../data/dataset-00-0.csv ../data/dataset-00-1.csv 5`

## Old Workflow

1. `extract_features`:  Read tweets from `election_day_tweets` and `troll-tweets`
2. `wikidata`: Vectorize into `tweets_output`
3. `cleaningDataSet.R`: troll-weets -> `dataset`, election_day_tweets -> `cleaned_elec2.csv`

## Data

election_day_tweets header:
0. text
1. created_at
2. geo
3. lang
4. place
5. coordinates
6. user.favourites_count
7. user.statuses_count
8. user.description
9. user.location
10. user.id
11. user.created_at
12. user.verified
13. user.following
14. user.url
15. user.listed_count
16. user.followers_count
17. user.default_profile_image
18. user.utc_offset
19. user.friends_count
20. user.default_profile
21. user.name
22. user.lang
23. user.screen_name
24. user.geo_enabled
25. user.profile_background_color
26. user.profile_image_url
27. user.time_zone
28. id
29. favorite_count
30. retweeted
31. source
32. favorited
33. retweet_count

output+
34 created_str
35 hashtags
36 mentions

`extracting_features.py` converts `election_day_tweets.csv` to `election_day_tweets_output.csv`


0. user_id
1. user_key
2. created_at
3. created_str
4. retweet_count
5. retweeted
6. favorite_count
7. text
8. tweet_id
9. source
10. hashtags
11. expanded_urls
12. posted
13. mentions
14. retweeted_status_id
15. in_reply_to_status_id
