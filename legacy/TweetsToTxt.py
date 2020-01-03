#For NatLan Processing
#By E.T. Kortela
import csv

#file location parameters
jennyenicholson_tweets = "tweets/jennyenicholson.csv" #JennyENicholson
foldablehuman_tweets = "tweets/foldablehuman.csv" #FoldableHuman
ninevolt_tweets = "tweets/9volt.csv" #9_volt_
yingjuechen_tweets = "tweets/yingjuechen.csv" #YingjueChen
marinscos_tweets = "tweets/marinscos.csv" #marinscos

#Calculate average sentiment for all tweets in an account
def calculateAverageSentiment(fileLocation):
    with open(fileLocation, newline='', encoding='utf8') as csv_file:
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

#Make a txt-file containing all tweets in an account for the Mairesse program
def tweetsToTxt(txtFileLocation, csvFileLocation):
    file = open(txtFileLocation,'w', encoding='utf-8')
    line_count = 0
    with open(csvFileLocation, newline='', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count != 0:
                file.write(row[2])
            line_count += 1

#Make a txt-file for each individual tweet in an account for the Mairesse program
def tweetsToIndividualTxt(path, csvFileLocation):
    with open(csvFileLocation, newline='', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                int(row[0])
                fileName = path + row[0] + '.txt'
                file = open(fileName,'w', encoding='utf-8')
                file.write(row[2])
            except ValueError:
                continue


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

tweetsToTxt('tweets/jennyenicholsonAllTweets.txt', jennyenicholson_tweets)
tweetsToTxt('tweets/foldablehumanAllTweets.txt', foldablehuman_tweets)
tweetsToTxt('tweets/ninevoltAllTweets.txt', ninevolt_tweets)
tweetsToTxt('tweets/yingjuechenAllTweets.txt', yingjuechen_tweets)
tweetsToTxt('tweets/marinscosAllTweets.txt', marinscos_tweets)

tweetsToIndividualTxt('tweets/9volt/', ninevolt_tweets)
tweetsToIndividualTxt('tweets/jennyenicholson/', jennyenicholson_tweets)
tweetsToIndividualTxt('tweets/foldablehuman/', foldablehuman_tweets)
tweetsToIndividualTxt('tweets/yingjuechen/', yingjuechen_tweets)
tweetsToIndividualTxt('tweets/marinscos/', marinscos_tweets)
