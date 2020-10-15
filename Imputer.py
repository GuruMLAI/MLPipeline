#! /usr/bin/python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons


class VarImputer:
    """This class defines imputation methods, stores imputation values and performs imputation of training and test data"""

    def __init__(self):
        self.ImputeTable=pd.DataFrame(columns=['Variable','ImputeMethod','ImputeCode'])
        self.dict = {}
        print("\nNew Variable Imputer Object defined")

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

    def draw_histograms(self, df, variables, updateimp=True):

        if variables == []:
            print('Plotting Histograms for all variables\n\n')
            variables = df.columns

        for j in variables:
            Imp_Type = self.ind_hist(df,j)
            if updateimp:
                self.dict.update({j:Imp_Type})


    def imp_define(self, df, variables, output=''):
        self.draw_histograms(df, variables)

        row_list=[]
        for a_key in self.dict:
            if self.dict.get(a_key) == 'Median':
                ImpVal = df[a_key].median()
                row_list.append([a_key,self.dict.get(a_key),"{{arg1}}['{arg2}_Imp']={{arg1}}['{arg2}'].fillna({arg3})"\
                .format(arg1='',arg2=a_key,arg3=ImpVal)])
            elif self.dict.get(a_key) == 'Mode':
                ImpVal = df[a_key].mode()[0]
                if isinstance(ImpVal, str):
                    ImpVal = "'" + ImpVal + "'"
                row_list.append([a_key,self.dict.get(a_key),"{{arg1}}['{arg2}_Imp']={{arg1}}['{arg2}'].fillna({arg3})"\
                    .format(arg1='',arg2=a_key,arg3=ImpVal)])


        to_append = pd.DataFrame(row_list,columns=['Variable','ImputeMethod','ImputeCode'])

        self.ImputeTable = self.ImputeTable.append(to_append,ignore_index=True)

        if output != '':
            self.ImputeTable.to_csv(output,index=False)

        print('Imputation Parameters have been defined')


    def imp_apply(self, df, input=''):
        
        if input != '':
            self.ImputeTable = pd.read_csv(input)

        if self.ImputeTable.shape[0] == 0:
            print('No Imputations have been defined in this VarImputer Instance.\nPlease use the imp_define method if necessary.\nNo imputation will be performed.')
        else:
            for index, row in self.ImputeTable.iterrows():
                #print('{}\n{}\n{}'.format(row[0],row[1],row[2].format(arg1=df.name)))
                exec(row[2].format(arg1='df'))
                df.drop(row[0],axis=1,inplace=True)
