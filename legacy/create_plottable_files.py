# By K.P.
import os

def createPlottable(path, acc):
    fl = 'Plottable/' + acc + '_plottable + '.txt'
    with open(fl, 'w') as destination:
        for file in sorted(os.listdir(path)):
            path = 'Final_values_v2/Individual_tweets/' + acc
            filename = os.fsdecode(file)
            path = path + '/' + filename

            row = []
            with open(path, 'r') as f:
                line = f.readline().split(',')
                for i in line:
                    row.append(float(i))

            destination.write(' '.join(str(num) for num in row))
            destination.write('\n')
            
        
def main():
    folders = ['9volt', 'foldablehuman', 'jennyenicholson', 'marinscos', 'yingjuechen']
    
    for acc in folders:
        path = 'Final_values_v2/Individual_tweets/' + acc
        folder = os.fsencode(path)
        
        createPlottable(path, acc)


if __name__ == "__main__":
    main()
