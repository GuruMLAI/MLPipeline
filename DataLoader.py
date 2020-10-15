#! /usr/bin/python3
import os, sys
from tkinter import Tk
from tkinter.filedialog import askdirectory
import numpy as np
import pandas as pd


class DataLoader:
    '''
    This can be used for loading the data.
    The user has to choose the folder where the training and the test data are located.
    Also specify the names of the files. The default file format is assumed to be csv.
    The __init__ method defines the data directory and the training and test files.
    The load method does the loading of the data into train and test datasets.
    Alternatively, the user can also directly specify a pathusing the run_params 'Data_Location'
    '''

    def __init__(self,loc = 'User_Defined', train='train.csv', test='test.csv'):

        if loc == 'User_Defined':
            print('Please select the directory that has the data.')
            Tk().withdraw()
            self.data_path = askdirectory()
        elif os.path.exists(loc):
            self.data_path = loc
        else:
            print('The specified path does not exist. Please correct it and try again')
            sys.exit(1)


        self.train_data = os.path.join(self.data_path, train)
        self.test_data = os.path.join(self.data_path, test)
        print("\nNew Data Loader Object defined")

    def load(self):
        temp1, temp2 = pd.read_csv(self.train_data), pd.read_csv(self.test_data)
        print('The data has been loaded.\n')
        return temp1, temp2
