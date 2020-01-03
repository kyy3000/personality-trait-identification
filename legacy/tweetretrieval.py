# Dylan's MacbookPro #
# JP DILAN KALPA - 11634268 #
# Modified for NatLan Processing by E.T.Kortela #
import os
import pandas as pd
import tweepy
import re
import string
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


#Twitter credentials for the app
consumer_key = 'xxxxx'
consumer_secret = 'xxxxx'
access_key= 'xxxxx'
access_secret = 'xxxxx'

#pass twitter credentials to tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#file location for clearer path
jennyenicholson_tweets = "tweets/jennyenicholson.csv" #JennyENicholson
foldablehuman_tweets = "tweets/foldablehuman.csv" #FoldableHuman
ninevolt_tweets = "tweets/9volt.csv" #9_volt_
yingjuechen_tweets = "tweets/yingjuechen.csv" #YingjueChen
marinscos_tweets = "tweets/marinscos.csv" #marinscos

#columns of the csv file
COLS = ['id', 'created_at', 'original_text','clean_text','polarity']

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

#Emoji patterns
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)

#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)


#method clean_tweets()
def clean_tweets(tweet):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(tweet)

    #after tweepy preprocessing the colon left remain after removing mentions
    #or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)
    #replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)

    #remove emojis from tweet
    tweet = emoji_pattern.sub(r'', tweet)

    #filter using NLTK library append it to a string
    filtered_tweet = []

    #looping through conditions
    for w in word_tokens:
        #check tokens against stop words , emoticons and punctuations
        if w not in stop_words and w not in emoticons and w not in string.punctuation:
            filtered_tweet.append(w)
    return ' '.join(filtered_tweet)
    #print(word_tokens)
    #print(filtered_sentence)

#method write_tweets()
def write_tweets(username, file):
    # If the file exists, then read the existing data from the CSV file.
    if os.path.exists(file):
        df = pd.read_csv(file, header=0)
    else:
        df = pd.DataFrame(columns=COLS)
    #page attribute in tweepy.cursor and iteration, removed since=start_date
    for page in tweepy.Cursor(api.user_timeline, id=username, include_rts=False, tweet_mode="extended").pages():
        for status in page:
            new_entry = []
            status = status._json

            ## check whether the tweet is in english or skip to the next tweet
            if status['lang'] != 'en':
                continue

            #tweepy preprocessing called for basic preprocessing
            #clean_text = p.clean(status['text'])

            #call clean_tweet method for extra preprocessing
            filtered_tweet=clean_tweets(status['full_text'])

            #pass textBlob method for sentiment calculations
            blob = TextBlob(filtered_tweet)
            #Sentiment = blob.sentiment

            #seperate polarity and subjectivity in to two variables
            polarity = blob.sentiment.polarity
            #subjectivity = Sentiment.subjectivity

            #new entry append
            new_entry += [status['id'], status['created_at'],
                          status['full_text'],filtered_tweet, polarity]

            #to append original author of the tweet
            #new_entry.append(status['user']['screen_name'])

            single_tweet_df = pd.DataFrame([new_entry], columns=COLS)
            df = df.append(single_tweet_df, ignore_index=True)
            csvFile = open(file, 'a' ,encoding='utf-8')
    df.to_csv(csvFile, mode='a', columns=COLS, index=False, encoding="utf-8",  line_terminator='\n')

#call main method passing keywords and file path
names = ["JennyENicholson", "FoldableHuman", "9_volt_", "YingjueChen", "marinscos"]
files = [jennyenicholson_tweets, foldablehuman_tweets, ninevolt_tweets, yingjuechen_tweets, marinscos_tweets]

for x in range(len(names)):
	write_tweets(names[x], files[x])
