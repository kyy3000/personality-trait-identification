import csv

#file location macros
jennyenicholson_tweets = "tweets/jennyenicholson.csv" #JennyENicholson
foldablehuman_tweets = "tweets/foldablehuman.csv" #FoldableHuman
ninevolt_tweets = "tweets/9volt.csv" #9_volt_
yingjuechen_tweets = "tweets/yingjuechen.csv" #YingjueChen
marinscos_tweets = "tweets/marinscos.csv" #marinscos

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
'''