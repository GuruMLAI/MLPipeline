#! /usr/bin/python3

import numpy as np
import pandas as pd
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
