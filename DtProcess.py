import os, sys
from tkinter import Tk
from tkinter.filedialog import askdirectory
import math

import numpy as np
import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons


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

    def load(self):

        return pd.read_csv(self.train_data), pd.read_csv(self.test_data)


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

def get_grid_size(n):
    i,j = 1,1
    while i*j<n:
        if i == j:
            i += 1
        elif i == j+1:
            j += 1
    return i,j


#Plot a histogram and take options

class VarImputer:
    """This class defines imputation methods, stores imputation values and performs imputation of training and test data"""

    def __init__(self):
        self.ImputeTable=pd.DataFrame(columns=['Variable','ImputeMethod','ImputeCode'])
        self.dict = {}
        print("New Variable Imputer Object defined")

    def ind_hist(self,df,var_name):
        fig=plt.figure()
        ax=fig.add_subplot()
        plt.subplots_adjust(left=0.3)
        df[var_name].hist(bins=10,ax=ax)
        ax.set_title("{} - Missing Values: {:.1f} %".format(var_name, df[var_name].isnull().sum()*100/df.shape[0]))

        axcolor = 'lightgoldenrodyellow'
        rax = plt.axes([0.05, 0.5, 0.15, 0.15], facecolor=axcolor)
        radio = RadioButtons(rax, ('None', 'Median', 'Mode'))
        plt.show()

        return radio.value_selected

    def draw_histograms(self, df, variables):

        if variables == []:
            print('Plotting Histograms for all variables')
            variables = df.columns

        n_grids = math.ceil(len(variables)/4)
        for j in np.arange(n_grids):
            vars_now = variables[j*4:(j+1)*4]

            for i, var_name in enumerate(vars_now):
                Imp_Type = self.ind_hist(df,var_name)
                self.dict.update({var_name:Imp_Type})


    def define(self, df, variables):
        self.draw_histograms(df, variables)
        print(self.dict)
        row_list=[]
        for a_key in self.dict:
            if self.dict.get(a_key) == 'Median':
                ImpVal = df[a_key].median()
                row_list.append([a_key,self.dict.get(a_key),"{arg1}['{arg2}_Imp']={arg1}['{arg2}'].fillna({arg3})"\
                .format(arg1=df.name,arg2=a_key,arg3=ImpVal)])
            elif self.dict.get(a_key) == 'Mode':
                ImpVal = df[a_key].mode()[0]
                if isinstance(ImpVal, str):
                    ImpVal = "'" + ImpVal + "'"
                row_list.append([a_key,self.dict.get(a_key),"{arg1}['{arg2}_Imp']={arg1}['{arg2}'].fillna({arg3})"\
                    .format(arg1=df.name,arg2=a_key,arg3=ImpVal)])


        to_append = pd.DataFrame(row_list,columns=['Variable','ImputeMethod','ImputeCode'])

        self.ImputeTable = self.ImputeTable.append(to_append,ignore_index=True)

        self.ImputeTable.to_csv('abc.csv')

        print('Imputation Parameters have been defined')
