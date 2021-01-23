import pandas as pd
import random
import csv
import numpy as np
import pickle


dictCountry = {}
city_spaces = 70000
countryspaces = 250
TotalX = 1
TotalY=1
dictSamples = {}

def main():
    global dictSamples
    GenerateInput('../Adrian_test/NewTrain.csv')
    ExportDictionary(dictSamples)


def GenerateInput(path):
    """
    This function prepares the CSV file to the input format for the model
    1. Encodes the city: ~65000 booleans
    2. Encodes the country of destination: ~250 booleans
    3. Encodes the country of origin: ~250 booleans
    4. Days at previous stay: 1 integer
    5. Total stations of the trip: 1 integer
    6. Current station of the trip: 1 integer
    :param path: path to the train file
    :return: a tuple containing input x and output y
    """

    #we link to global variables
    global city_spaces
    global countryspaces

    #First it loads the training set
    #path = '../Adrian_test/NewTrain.csv'
    dataset = pd.read_csv(path)

    #it stores the value of the last row and initialize with first row
    lastrow = dataset.shape[0]
    lastrow=701227


    row = 0

    #station is zero at the beginning
    stations=0

    # we initialize the values for the next trip
    TotalStay = np.zeros((city_spaces + 2 * countryspaces + 10, 1), dtype=np.uint8)



    #numpy position with the number of stays
    PosStation = city_spaces+2*countryspaces

    # numpy position with the total number of stays
    PosTotStation = PosStation+1

    #numpy position with the number of nights of the stay
    PosNights = PosTotStation+1


    #tracking the trip_ID is necessary to know when there is a new sequence
    next_trip_ID = dataset.iloc[row+1, 9]

    while row <lastrow:
        # we store the ID of the trip into a variable
        current_trip_ID = dataset.iloc[row, 9]
        next_trip_ID = dataset.iloc[row + 1, 9]

        # we store the country of the trip into a variable
        hotel_country = dataset.iloc[row, 8]
        hotel_country_ID = city_spaces + GetCountryID(hotel_country)

        # same with the country of the booker
        booker_country = dataset.iloc[row, 7]
        booker_country_ID = city_spaces + countryspaces + GetCountryID(booker_country)

        # we get the number of nights
        nights = GetNights(dataset.iloc[row, 2],dataset.iloc[row, 3])

        # gets the new cityID
        city_ID = dataset.iloc[row, 4]

        # if it is the same trip, we can add the current line to the input information
        if (current_trip_ID == next_trip_ID):

            # we increase the quantity of stations
            stations = stations +1

            #create a new Stay_ID numpy data for this stay
            Stay_ID = np.zeros((city_spaces+2*countryspaces+10,1), dtype=np.uint8)

            #we put the available information
            Stay_ID[city_ID,0]=1
            Stay_ID[hotel_country_ID,0]=1
            Stay_ID[booker_country_ID,0] = 1
            Stay_ID[PosStation,0] = stations
            Stay_ID[PosNights,0] = nights

            #we add it to the total stay matrix
            TotalStay=np.hstack((TotalStay,Stay_ID))


            if stations==1:
                #this is the first stay, so we have to delete the first column
                TotalStay = np.delete(TotalStay,0,1)


        else:
            #next line will be a new trip, so the current line is the solution!

            #it generate the solution
            LastStay = np.zeros(city_spaces, dtype=np.uint8)
            LastStay[city_ID]=0

            #this function stores the result properly
            #not sure yet how it will be done
            StoreResult(TotalStay,LastStay)

            #we initialize the values for the next trip
            TotalStay=np.zeros((city_spaces+2*countryspaces+10,1), dtype=np.uint8)
            stations=0


        row = row +1


        #this simply prints an update of the percentage
        if row % (lastrow/100) == 0:
            print('completion rate: ',row//(lastrow/100))













def StoreResult(TotalStay,LastStay):
    """
    This function stores the result of the current iterations
    :param TotalStay:
    :param LastStay:
    :return:
    """

    global dictSamples

    #Check how many stations were done
    stations = TotalStay.shape[1]

    if stations in dictSamples:
        #there are already trips with this dimension, we add one
        dictSamples[stations]["X"] = np.concatenate((dictSamples[stations]["X"], TotalStay[None]), axis=0)
        dictSamples[stations]["Y"] = np.concatenate((dictSamples[stations]["Y"], LastStay[None]), axis=0)


    else:
        dictAux={
            "X": np.expand_dims(TotalStay,axis=0),
            "Y": np.expand_dims(LastStay, axis=0)
        }

        dictSamples[stations]=dictAux






def GetNights(start,end):
    """
    Based on the two input dates, returns how many nights were booked
    :param start: initial date
    :param end: final date
    :return: integer, number of nights
    """
    #To be implemented
    return(1)

def GetCountryID(country):
    """
    Given a country name, it looks in the dictionary of countries
    :param country: country name
    :return: integer
    """

    global city_spaces

    if country in dictCountry:
        return(dictCountry[country])

    else:
        #if it is not yet in the dictionary of countries we add it with the new id
        #new id is length of the dictionary of the maximum quantity of variables
        #if countryspaces is 250, then IDs will be 0, 1, ..., 249
        dictCountry[country]=min(len(dictCountry),countryspaces-1)
        return(dictCountry[country])


def ExportDictionary(dictSamples):
    a_file = open("dictSamples", "wb")
    pickle.dump(dictSamples,a_file)
    a_file.close()

if __name__ == '__main__':
    main()
