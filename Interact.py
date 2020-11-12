#! /usr/bin/python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
from itertools import combinations

'''
import os, sys
from tkinter import Tk
from tkinter.filedialog import askdirectory

import numpy as np
import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons
'''


class InteractionDefiner:
    '''
    This class defines the Interactions in the dataset between a defined set of input variables.
    The define_combination_interactor method defines the iterator which generates all the possible combinations of the variables
    that have been defined in features
    The type of interactions that are intended to be explored (e.g 2-way, 3-way etc.
     can be defined in types as a list
    '''

    def __init__(self):

        self.comb_interaction = False
        self.rank_interaction = False
        print('A new interaction definer has been created.')



    def define_combination_interactor(self, features, types, cat_var):

        self.comb_interaction = True
        self.comb_features = features
        self.comb_types = types
        self.comb_cat_var = cat_var

        self.comb_iterator = []
        for i in self.comb_types:
            for x in combinations(np.arange(len(self.comb_features)),i):
                self.comb_iterator.append(x)

    def define_rank_interactor(self, data, features, cat_var, output=''):

        self.rank_interaction = True
        self.rank_features = features
        self.rank_cat_var = cat_var
        self.rank_InteractTable = pd.DataFrame(columns=['Variable','Variable_Value']+self.rank_features)

        for i in self.rank_cat_var:
            sr_temp = data.groupby([i],as_index=False)[self.rank_features].mean()

            df_temp = pd.DataFrame(data=sr_temp)
            df_temp['Variable'] = i
            df_temp.rename(columns={i:'Variable_Value'},inplace=True)

            self.rank_InteractTable = self.rank_InteractTable.append(df_temp,ignore_index=True)

        if output != '':
            self.rank_InteractTable.to_csv(output,index=False)

        print('Rank Interactions have been defined')



    def calculate(self, data, rank_input=''):

        if self.comb_interaction:

            for i in self.comb_iterator:

                f_list = [self.comb_features[k] for k in list(i)]
                f_name = '_'.join(f_list)
                create = 1
                for j in self.comb_cat_var:
                    if f_name.count(j) > 1:
                        create = 0
                if create == 1:
                    data[f_name] = data[f_list].prod(axis=1)

            print('Combination Interactions have been applied to the data')

        if self.rank_interaction:
            if rank_input != '':
                self.rank_InteractTable = pd.read_csv(rank_input)

            self.rank_cat_var = list(set(self.rank_InteractTable['Variable']))
            self.rank_features_new = [i for i in list(self.rank_InteractTable.columns) if i not in ['Variable', 'Variable_Value']]

            for i in self.rank_cat_var:
                temp = self.rank_InteractTable[self.rank_InteractTable['Variable']==i].drop('Variable', axis=1)
                temp = temp.add_prefix(i+'_').add_suffix('_mean')

                data = pd.merge(data, temp, how='left', left_on=i, right_on=i+'_'+'Variable_Value_mean').drop(i+'_'+'Variable_Value_mean', axis=1)

            print('Rank Interactions have been applied to the data')
