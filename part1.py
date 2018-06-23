## Full Name: Daniella Raz
## Uniqname: drraz
## UMID: 86870313

import tweepy
import nltk
import json
import sys
import re
from collections import Counter
from nltk.corpus import stopwords
import string
import csv

# setting up command line input for python
user_name = sys.argv[1]
num_tweets = int(sys.argv[2])

# twitter authorization and API
consumer_key = "sv3ZL9NokYLUkIPSBdKkmCNGm"
consumer_secret = "6CmpBPHcIWqI26w1m5SKa1sAV40utYrbx0tFiWfYQaJ8esMd15"
access_token = "920998664629374978-KNoAq3hldeL4uMI88sGolIj2cr4SW4p"
access_token_secret = "FheeBQN6V0cbOOJgBY8GOTE7nNjxkfpz8SIl6rYYr1I6i"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

list_of_tweets = []
list_of_retweets = []
list_original_tweets = []
total_num_favorites = 0
total_num_retweets = 0

# retrieves only tweets of certain user and only certain number
# separates original from the retweets+originals to get full text of retweeted ones
for tweet in tweepy.Cursor(api.user_timeline,id=user_name,tweet_mode='extended').items(num_tweets):
    # selecting only the original tweets from the tweets, finding retweet and favorite count of only originals
    if not hasattr(tweet, 'retweeted_status'):
        total_num_favorites += tweet.favorite_count
        total_num_retweets += tweet.retweet_count
        list_original_tweets.append(tweet.full_text)
    # in order to get FULL text of tweet which the user themself did not tweet must get full_text within retweeted_status, not status
    if hasattr(tweet, 'retweeted_status'):
        list_of_retweets.append(tweet.retweeted_status.full_text)

# combining the list of original tweets' text with the list of retweets tweet text, to ensure getting full text of retweets
list_of_tweets = list_of_retweets + list_original_tweets
num_original_tweets = len(list_original_tweets)

# analyzing all tweets so turning list of separate tweet texts into one string
tweets_string = ' '.join(list_of_tweets)
# removing https, http links, hastags and @'s, numbers
tweets_string = re.sub('(\B[#|@]\w+)|((http)(s*)://[^\s]+)', '', tweets_string)
# removing numbers
tweets_string = re.sub(' \d+', '', tweets_string)
# removing emojis
# source: https://gist.github.com/Alex-Just/e86110836f3f93fe7932290526529cd1
emoji_pattern = re.compile("["u"\U00010000-\U0010ffff""]+", flags=re.UNICODE)
tweets_string = emoji_pattern.sub(r'', tweets_string)

# making stopwords list of rt and RT in addition to above regex and tokenizing
stop_words = ['rt', 'RT']
tokens = nltk.word_tokenize(tweets_string)

# removing words from tokens that are either stop words, emojis or simply punctuation
list_of_tokens = []
for token in tokens:
    if token not in stop_words and token not in string.punctuation:
        list_of_tokens.append(token)

# Part of Speech tagging and organizing, separating verbs, nouns and adjectives
list_of_pos = nltk.pos_tag(list_of_tokens)
list_of_verbs = []
list_of_nouns = []
list_of_adj = []
for word,pos in list_of_pos:
    if pos in ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'):
        list_of_verbs.append((word,pos))
    if pos in ('NN' ,'NNS', 'NNP', 'NNPS'):
        list_of_nouns.append((word,pos))
    if pos in ('JJ', 'JJS', 'JJR'):
        list_of_adj.append((word,pos))

# Counting occurrences of each verb, and sorting first by number of occurrence, then by alphabetical ascending order of the word, with capitalized preceding the lowercase version of the word if both exist
verb_counts = Counter(word for word,pos in list_of_verbs)
verb_counts = sorted(verb_counts.items(), key=lambda x: (-x[1],x[0].casefold()), reverse=False)
top_verbs = verb_counts[0:5]
# formatting to print out like sample: word(count) word(count) etc..
verb_list = []
for verb, count in top_verbs:
    count = str(count)
    verb = verb+"("+count+")"
    verb_list.append(verb)
verbs = " ".join(verb_list)

# Counting occurrences of each noun, and sorting first by number of occurrence, then by alphabetical ascending order of the word, with capitalized preceding the lowercase version of the word if both exist
noun_counts = Counter(word for word,pos in list_of_nouns)
noun_counts = sorted(noun_counts.items(), key=lambda x: (-x[1],x[0].casefold()), reverse=False)
top_nouns = noun_counts[0:5]
# formatting to print out like sample: word(count) word(count) etc..
noun_list = []
for noun, count in top_nouns:
    count = str(count)
    noun = noun+"("+count+")"
    noun_list.append(noun)
nouns = " ".join(noun_list)

# Counting occurrences of each adjective, and sorting first by number of occurrence, then by alphabetical ascending order of the word, with capitalized preceding the lowercase version of the word if both exist
adj_counts = Counter(word for word,pos in list_of_adj)
adj_counts = sorted(adj_counts.items(), key=lambda x: (-x[1],x[0].casefold()), reverse=False)
top_adj = adj_counts[0:5]
# formatting to print out like sample: word(count) word(count) etc..
adj_list = []
for adj, count in top_adj:
    count = str(count)
    adj = adj+"("+count+")"
    adj_list.append(adj)
adjectives = " ".join(adj_list)

# printing the information, and first 5 (aka most frequent given previous sorting) of verbs, nouns, adjectives
print("USER: ", user_name)
print("TWEETS ANALYZED: ", num_tweets)
print("VERBS: ", verbs)
print("NOUNS: ", nouns)
print("ADJECTIVES: ", adjectives)
print("ORIGINAL TWEETS: ", num_original_tweets)
print("TIMES FAVORITED (ORIGINAL TWEETS ONLY): ", total_num_favorites)
print("TIMES RETWEETED (ORIGINAL TWEETS ONLY): ", total_num_retweets)

# writing five most common nouns to a csv file
top_nouns = noun_counts[0:5]
top_nouns.insert(0, ("Noun", "Number"))
myFile = open('noun_data.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(top_nouns)
