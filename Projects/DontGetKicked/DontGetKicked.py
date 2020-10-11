#! /usr/bin/python3

import os, sys
from MLPipeline.DtProcess import DataLoader, Standardizer, VarImputer

dl = DataLoader(os.path.join(sys.path[0],'Data'),'training.csv','test.csv')

train_data, test_data = dl.load()
train_data.name = 'train_data'
test_data.name = 'test_data'


Imp = VarImputer()
#Imp.draw_histograms(train_data,train_data.columns.tolist())
#Imp.draw_histograms(train_data,['RefId', 'IsBadBuy', 'Auction'])
Imp.define(train_data, train_data.columns.tolist())
