import pandas as pd
import random
import csv
import numpy as np

NewID = 1
Result = []


def main():
    CalculateSolutions()


def CalculateSolutions():
    Result = []
    global NewID

    # we load test and transition matrices
    test = pd.read_csv('NewTest.csv')
    transition = pd.read_csv('conditional.csv')
    print(transition.head())

    # we move transition to a numpy
    transition = transition.to_numpy()
    print(transition[0])



    # we get the value of the last row
    lastrow = test.shape[0]

    # we start iterating the first row
    row = 0
    last_trip_ID = test.iloc[row, 9]

    # we load the TopCities file containing the reduced index
    LoadTopCities()

    DestinationInTrip = []

    while row < lastrow:

        # we store the ID of the trip into a variable
        current_trip_ID = test.iloc[row, 9]

        #if it is the same trip we add it to the list of previous cities
        if (current_trip_ID == last_trip_ID):
            #info about the present city which will be added to the DestinationInTrip list
            city_ID = test.iloc[row, 4]
            Reduced_ID = NewID[city_ID - 1]
            DestinationInTrip.append(Reduced_ID)

        # we check if the ID of the trip is the same we had in the last line, which means it is the same trip
        if not (current_trip_ID == last_trip_ID):
            # it is a new trip, we have to guess the destination for the previous line
            # we get the id of the city of row-2
            city_ID = test.iloc[row - 2, 4]

            # this ID is the booking ID. We converted it earlier using topcities
            Reduced_ID = NewID[city_ID-1]

            # this is the transition_row for the city
            DestRow = transition[Reduced_ID-1]

            # we delete the previous entry, since it is the destination which actually has to be predicted...
            # we also delete the one of the last visited city
            if(len(DestinationInTrip)>0):
                DestinationInTrip.pop()
            if (len(DestinationInTrip) > 0):
                DestinationInTrip.pop()


            Result.append(SelectDestination(DestRow,Reduced_ID,DestinationInTrip))

            DestinationInTrip = [Reduced_ID]

        last_trip_ID = current_trip_ID
        row = row + 1

    # File has completely been iterated
    with open("Result_basic_2.csv", "w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerows(Result)


def LoadTopCities():
    import pandas as pd
    import random
    import csv
    import openpyxl
    import numpy

    global NewID

    # we load TopCities_for_numpy which contains the reduced ID on the position of the BookingID
    wb = openpyxl.open('TopCities_for_numpy.xlsx')
    ws = wb.active
    data = ws.values

    # Get the first line in file as a header line
    columns = next(data)[0:]
    # Create a DataFrame based on the second and subsequent lines of data
    df = pd.DataFrame(data, columns=columns)

    # We store into NewID the numpy array
    NewID = df.to_numpy()



def SelectDestination(DestRow,Reduced_ID,DestinationInTrip):
    """
    This function returns the top 4 destinations
    It will exclude the 9999 since this does not actually belong to one city, but to all those 10% less frequented cities
    :param DestRow: Transition Row
    :return: An array with top 4 destinations
    """

    
    for city in DestinationInTrip:
        DestRow[0,city]=0

    # put the last column equal zero
    DestRow[0, 10000] = 0


    # position 0 is the row index
    DestRow[0, 0] = 0

    Top_1 = np.argmax(DestRow)
    DestRow[0, Top_1] = 0
    Top_2 = np.argmax(DestRow)
    DestRow[0, Top_2] = 0
    Top_3 = np.argmax(DestRow)
    DestRow[0, Top_3] = 0
    Top_4 = np.argmax(DestRow)
    DestRow[0, Top_4] = 0

    return (Top_1, Top_2, Top_3, Top_4)


if __name__ == '__main__':
    main()
