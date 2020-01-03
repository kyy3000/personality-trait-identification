#For NatLan Processing
#By E.T. Kortela

import csv

#file location macros
jennyenicholson_tweets = "tweets/jennyenicholson.csv" #JennyENicholson
foldablehuman_tweets = "tweets/foldablehuman.csv" #FoldableHuman
ninevolt_tweets = "tweets/9volt.csv" #9_volt_
yingjuechen_tweets = "tweets/yingjuechen.csv" #YingjueChen
marinscos_tweets = "tweets/marinscos.csv" #marinscos

#Calculate average sentiment of all tweets in an account
def calculateAverageSentiment(csvFileLocation):
    with open(csvFileLocation, newline='', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        tweets = 0
        sum = 0.0
        for row in csv_reader:
            try:
                sum += float(row[4])
                tweets += 1
            except ValueError:
                continue
        return sum/tweets

#Calculate number of tweets for account with the sentiment (polarity) of 0.0 as well as total number of tweets and percentage of neutrals out of total
def calculateNeutralTweets(csvFileLocation):
    neutralTweets = 0
    totalTweets = 0
    with open(csvFileLocation, newline='', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                if float(row[4]) == 0.0:
                    neutralTweets += 1
                totalTweets += 1
            except ValueError:
                continue
    return neutralTweets, totalTweets, neutralTweets/totalTweets*100

#Retrieve creation time, tweet text and sentiment for a tweet by id
def getTweetData(id, csvFileLocation):
    created_at = ''
    tweet = ''
    sentiment = 0.0
    with open(csvFileLocation, newline='', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                if id == int(row[0]):
                    created_at = row[1]
                    tweet = row[2]
                    sentiment = float(row[4])
                    break
                else:
                    continue
            except ValueError:
                continue
    return created_at, tweet, sentiment

'''
jennySentiment = calculateAverageSentiment(jennyenicholson_tweets)
print("JennyENicholson's average sentiment is " + str(jennySentiment))
foldableSentiment = calculateAverageSentiment(foldablehuman_tweets)
print("FoldableHuman's average sentiment is " + str(foldableSentiment))
ninevoltSentiment = calculateAverageSentiment(ninevolt_tweets)
print("9_volt_'s average sentiment is " + str(ninevoltSentiment))
yingSentiment = calculateAverageSentiment(yingjuechen_tweets)
print("YingjueChen's average sentiment is " + str(yingSentiment))
marincosSentiment = calculateAverageSentiment(marinscos_tweets)
print("marinscos's average sentiment is " + str(marincosSentiment))

created_at, tweet, sentiment = getTweetData(1204531191962988544, yingjuechen_tweets)
print(created_at)
print(tweet)
print(str(sentiment))

jennyNeutrals, jennyTotal, jennyPercentage = calculateNeutralTweets(jennyenicholson_tweets)
print("JennyENicholson's account has " + str(jennyNeutrals) + " tweets with neutral sentiment out of " + str(jennyTotal) + ". Their tweets are " + str(jennyPercentage) + "% neutral.")
foldableNeutrals, foldableTotal, foldablePercentage = calculateNeutralTweets(foldablehuman_tweets)
print("FoldableHuman's account has " + str(foldableNeutrals) + " tweets with neutral sentiment out of " + str(foldableTotal) + ". Their tweets are " + str(foldablePercentage) + "% neutral.")
ninevoltNeutrals, ninevoltTotal, ninevoltPercentage = calculateNeutralTweets(ninevolt_tweets)
print("9_volt_'s account has " + str(ninevoltNeutrals) + " tweets with neutral sentiment out of " + str(ninevoltTotal) + ". Their tweets are " + str(ninevoltPercentage) + "% neutral.")
yingNeutrals, yingTotal, yingPercentage = calculateNeutralTweets(yingjuechen_tweets)
print("YingjueChen's account has " + str(yingNeutrals) + " tweets with neutral sentiment out of " + str(yingTotal) + ". Their tweets are " + str(yingPercentage) + "% neutral.")
marincosNeutrals, marincosTotal, marincosPercentage = calculateNeutralTweets(marinscos_tweets)
print("marinscos's account has " + str(marincosNeutrals) + " tweets with neutral sentiment out of " + str(marincosTotal) + ". Their tweets are " + str(marincosPercentage) + "% neutral.")
totalNeutralAverage = (jennyPercentage + foldablePercentage + ninevoltPercentage + yingPercentage + marincosPercentage) / 5
print("The average percentage of tweets with a sentiment of 0.0 among all five accounts is " + str(totalNeutralAverage))
'''
