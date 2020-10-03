#! /usr/bin/python3

import os, sys
from MLPipeline.DtProcess import DataLoader, Standardizer, draw_histograms

dl = DataLoader(os.path.join(sys.path[0],'Data'),'training.csv','test.csv')

train_data, test_data = dl.load()

draw_histograms(train_data,train_data.columns[0:5].tolist())
