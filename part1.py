#Full Name: Daniella Raz
#Uniqname: drraz
#UMID: 86870313

# library imports
import tweepy
import nltk
import json
import sys
import re
from collections import Counter
from nltk.corpus import stopwords
import string

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
# separates original from the retweets+originals
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

# analyzing all tweets thus turning list of separate tweet texts into one string
tweets_string = ' '.join(list_of_tweets)

# removing https, http links
tweets_string = re.sub('(http)(s*)://[^\s]+', '', tweets_string)
# removing hashtags and @
tweets_string = re.sub('\B[#|@]\w+', '', tweets_string)
# removing numbers and words starting with number
tweets_string = re.sub('\d\w+', '', tweets_string)

#making stopwords list, adding rt and RT, and tokenizing
stop_words = stopwords.words('english') + ['rt', 'RT']
tokens = nltk.word_tokenize(tweets_string)

#removing words from tokens that are either stop words or simply punctuation
list_of_tokens = []
for token in tokens:
    if token not in stop_words and token not in string.punctuation:
        list_of_tokens.append(token)

list_of_pos = nltk.pos_tag(tokens)


#print([(word, tag) for word, tag in list_of_pos if tag in ('NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJS', 'JJR')])


# printing the information
print("USER: ", user_name)
print("TWEETS ANALYZED: ", num_tweets)
print("VERBS: ")
print("NOUNS: ")
print("ADJECTIVES: ")
print("ORIGINAL TWEETS: ", num_original_tweets)
print("TIMES FAVORITED (ORIGINAL TWEETS ONLY):", total_num_favorites)
print("TIMES RETWEETED (ORIGINAL TWEETS ONLY):", total_num_retweets)
