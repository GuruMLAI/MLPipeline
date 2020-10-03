#! /usr/bin/python3

import os, sys
from MLPipeline.DtProcess import DataLoader


dl = DataLoader(os.path.join(sys.path[0],'Data'),'training.csv','test.csv')
train_data, test_data = dl.load()

print(train_data.head())
