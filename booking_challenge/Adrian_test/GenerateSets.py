"""
This function splits the training set into two sets:
- A train set
- A test set

This can be helpful to train the model and test it afterwards knowing the result

The training set given by booking can be used as validation set
"""

import pandas as pd
import random
import csv

train = 0
TEST_RATIO = 0.4
NewTrain = []
NewTest = []


def ProcessLine(row, assignment):
    global NewTrain
    global NewTest
    global train

    row_content = []
    col = 0

    #put the row into a list
    while col < 9:
        row_content.append(train.iloc[row,col])
        col = col +1


    #Input row from the original train set is to be added to the new train set
    if assignment=="train":
        NewTrain.append(row_content)

    else:
        NewTest.append(row_content)



def main():
    global train
    global NewTrain
    global NewTest
    global conditional



    #load train data
    train = pd.read_csv('../booking_train_set.csv')


    last_trip_ID = None

    #we get the value of the last row
    lastrow = train.shape[0]

    #we start iterating the first row
    row = 1

    while row<lastrow:
        #we store the ID of the trip into a variable
        current_trip_ID = train.iloc[row,9]

        # we check if the ID of the trip is the same we had in the last line, which means it is the same trip
        if current_trip_ID==last_trip_ID:
            #if it is the same trip we will perform an operation
            ProcessLine(row,assignment)
        else:
            #it is a new trip, we have to choose if it is assigned to the train or to the test set
            dice = random.random()
            if dice < TEST_RATIO:
                assignment = "Test"
            else:
                assignment = "Train"

            ProcessLine(row,assignment)

        last_trip_ID=current_trip_ID
        row = row +1


    #File has completely been iterated
    with open("NewTrain.csv","w",newline="") as output:
        writer = csv.writer(output)
        writer.writerows(NewTrain)

    with open("NewTest.csv","w",newline="") as output:
        writer = csv.writer(output)
        writer.writerows(NewTest)



if __name__ == '__main__':
    main()






