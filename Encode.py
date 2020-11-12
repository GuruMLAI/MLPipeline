#! /usr/bin/python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons


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
