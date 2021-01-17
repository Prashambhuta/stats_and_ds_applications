import pandas as pd
import numpy as np
import math

dict_reduced = {}
train = 0
nr_cities = 0
max_id = 0
conditional = 0


def main():
    global train
    global nr_cities
    global max_id
    global conditional

    #load train data
    train = pd.read_csv('../booking_train_set.csv')

    TopCities = pd.DataFrame

    TopCities=train.groupby("city_id").count()
    TopCities.to_excel("TopCities.xlsx")

if __name__ == '__main__':
    main()

