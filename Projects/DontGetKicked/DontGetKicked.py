#! /usr/bin/python3

import os, sys
from MLPipeline.DataLoader import DataLoader
from MLPipeline.Imputer import VarImputer
#Standardizer

dl = DataLoader(os.path.join(sys.path[0],'Data'),'training.csv','test.csv')

train_data, test_data = dl.load()
train_data.name = 'train_data'
test_data.name = 'test_data'


Imp = VarImputer()
Imp.imp_define(train_data, ['Trim'], output='impute_definitions.csv')
Imp.imp_apply(train_data,input='impute_definitions.csv')
