#! /usr/bin/python3
import os, sys
from tkinter import Tk
from tkinter.filedialog import askdirectory

import numpy as np
import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons




class Standardizer:

    def __init__(self, method='stddev'):
        self.method = method


    def define(self, data, var_list):

        std_list = []
        for i in var_list:
            if self.method == 'stddev':
                std_list.append((i, data[i].mean(), data[i].std()))
            else:
                std_list.append((i, data[i].min(), data[i].max()-data[i].min()))

        self.std_list = std_list


    def calculate(self, data):
        for i in self.std_list:
            var, num, den = i
            nm = 'std_' + var
            data[nm] = data[var].apply(lambda x: (x-num)/den)

            data.drop(var, axis=1, inplace=True)

        return data



class Encoder:
    def __init__(self,features):
        self.features = features

    def find_values(self, train_data):
        feature_values = {}
        for i in self.features:
            feature_values.update({i:list(train_data[i].unique())})
        self.feature_values = feature_values

        print('Unique values of the encoded variables are :\n {}'.format(self.feature_values))
        print('Dummy variables will be created using all but the first value in the list\n')

    def encode(self, data):
        for key, value in self.feature_values.items():
            for i in np.arange(1,len(value)):
                var_name = str(key)+'_'+str(value[i])
                data[var_name] = data[key].apply(lambda x: 1 if x == value[i] else 0)
            data.drop(key, axis=1, inplace=True)

        return data




class InteractionDefiner:
    '''
    This class defines the Interactions in the dataset between a defined set of input variables.
    The __init__ method defines the iterator which generates all the possible combinations of the variables
    that have been defined in features
    The type of interactions that are intended to be explored (e.g 2-way, 3-way etc.
     can be defined in types as a list
    '''

    def __init__(self, features, types, cat_var):

        self.features = features
        self.types = types
        self.cat_var = cat_var

        self.iterator = []
        for i in self.types:
            for x in combinations(np.arange(len(self.features)),i):
                self.iterator.append(x)

    def calculate(self, data):

        for i in self.iterator:

            f_list = [self.features[k] for k in list(i)]
            f_name = '_'.join(f_list)
            create = 1
            for j in self.cat_var:
                if f_name.count(j) > 1:
                    create = 0
            if create == 1:
                data[f_name] = data[f_list].prod(axis=1)

        return data
