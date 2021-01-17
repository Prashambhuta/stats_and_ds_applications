import pandas as pd
import numpy as np
import openpyxl as xl

dictTopCities={}
train = 0
TransitionMatrix = np.zeros((10000,10000),dtype=np.uint32)

def ImportTopCities():
    global dictTopCities
    wb=xl.load_workbook('TopCities.xlsx')
    ws=wb.active
    for row in ws.iter_rows():
        dictTopCities[row[0].value]=row[1].value


def TransitionMatrixGen():

    global train
    global dictTopCities
    global TransitionMatrix

    # load train data
    train = pd.read_csv('../booking_train_set.csv')
    print(train.head())

    """
    last: city id of last line
    last_edit: edited city id of last line
    lastID: trip ID of last line's trip
    """
    last = None
    last_edit = None
    lastID = None

    """
    All line will be iterated
    lastrow: read from the shape
    """
    row = 0
    lastrow = train.shape[0]

    #completion: percentage used to print updates
    completion = 0

    TransitionMatrix = np.zeros((10000,10000),dtype=np.uint32)

    while row < lastrow:
        #we get the ID of the new line
        new = train.iloc[row,9]
        newID = train.iloc[row, 4]

        #we get the reduced ID. Should the newID not exist, we take generic 9999
        if new in dictTopCities:
            new_edit = 9999
        else:
            new_edit = dictTopCities[newID]

        #update transition matrix
        if last == new:
            TransitionMatrix[last_edit,new_edit] = TransitionMatrix[last_edit,new_edit]+1

        #we go to the next line, before that we update the "last" values
        lastID=newID
        last_edit = new_edit
        last=new
        row = row +1

        if row % (lastrow//100) == 0:
            completion = completion +1
            print(completion)

    print(TransitionMatrix)
    result = pd.DataFrame(TransitionMatrix)
    result.to_csv("conditional.csv")





def main():
    ImportTopCities()
    TransitionMatrixGen()
    print("finished")

if __name__ == '__main__':
    main()