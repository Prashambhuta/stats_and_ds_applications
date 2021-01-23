"""
This file runs through a file called "NewTest.csv" contained in the same folder. It has to have the bookingchallenge structure
It loops and for each reservation it will extract the trip_id, the last city and the country of that hotel
Finally it will store this information into a file called NewTrainSolutions
"""
import pandas as pd
import random
import csv



def main():
    global NewTest

    # We create a list with another list inside containing the headers
    NewTestSolution = [["utrip_id", "city_id", "hotel_country"]]



    #load train data
    NewTest = pd.read_csv('NewTest.csv')

    #we get the value of the last row
    lastrow = NewTest.shape[0]
    print(lastrow)

    # we start iterating the first row
    row = 0

    #We initialize the value
    last_trip_ID = NewTest.iloc[row,9]

    while row < lastrow:
        # we store the ID of the trip into a variable

        current_trip_ID = NewTest.iloc[row, 9]

        #if the id is not the same we have to check the value of last trips final city
        if not current_trip_ID == last_trip_ID:
            trip_value=[]
            trip_value.append(NewTest.iloc[row - 1, 9])
            trip_value.append(NewTest.iloc[row - 1, 4])
            trip_value.append(NewTest.iloc[row - 1, 8])

            NewTestSolution.append(trip_value)

        last_trip_ID=current_trip_ID
        row = row+1



    #File has completely been iterated
    with open("NewTrainSolutions.csv","w",newline="",encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerows(NewTestSolution)

if __name__ == '__main__':
    main()