# By K.P.
import os
import numpy as np
import pandas as pd
import statistics


def extractValues(filename):
    model = []
    
    # read lines from a file into array
    with open(filename, 'r') as f:
        for line in f.readlines()[94:]:        
            account = []
            account.append(line)
            model.append(account)

    # discard everything except:
    # account name
    # personality values
    valueArray = []
    for account in model:
        
        temp = []
        account[0].replace('"', "")
        account = account[0].split(",")
        
        t = []
        t = list(account[0])
        x = []
        for i in reversed(t):
            if i != '\\':
                x.append(i)
            else:
                break

        x.reverse()
        x = x[:-5]
        temp.append(("".join(x)))

        for i in range(5):
            temp.append(float(account[-5+i]))

        valueArray.append(temp)

    return valueArray

# get an average for each four value set
def calculateAverages(account):
    averages = []
    averages.append(account[0]) # account name

    for i in range(0,5):
        temp = []
        for model in account[1:]:
            temp.append(model[i])
        averages.append(temp)
    
    for i in range(1,len(averages)):
        temp = statistics.mean(averages[i])
        averages[i] = temp

    return averages

# save the created array as a file
# filename: id
# row: five personality values, averagd between the four models
def createFile(account, acc):
    path = 'Final_values/Individual_tweet_values/' + acc
    filename = account[0].strip('\\')
    pathToFile = os.path.join(path, filename + ".txt")

    f = open(pathToFile, "w")
    values = ','.join(map(str, account[1:]))

    f.write(values)
    f.close()


def main():
    folders = ['9volt', 'foldablehuman', 'jennyenicholson', 'marinscos', 'yingjuechen']
    
    for acc in folders:
        path = 'All_personality_values/Individual_tweet_values/' + acc
        folder = os.fsencode(path)
        filenames = []
        modelArray = []
        values = []

        for file in os.listdir(folder):
            path = 'All_personality_values/Individual_tweet_values/' + acc

            filename = os.fsdecode(file)
            filenames.append(filename)

            path = path + '/' + filename
            values = extractValues(path)
            modelArray.append(values)
        
        sortedArray = []
        for i in range(len(values)):
            temp = []
            for m in modelArray:
                temp.append(m[i])
            sortedArray.append(temp)
        
        temp = []
        for account in sortedArray:
            acc = []
            accountName = account[0][0]
            acc.append(accountName)
            for model in account:
                acc.append(model[-5:])
            temp.append(acc)
        
        averages = []
        for d in temp:
            arr = calculateAverages(d)
            averages.append(arr)
        
        for a in averages:
            createFile(a, acc)
    

if __name__ == "__main__":
    main()
