#! /usr/bin/python3

import os, sys
from MLPipeline.DataLoad import DataLoader
from MLPipeline.Impute import VarImputer
from MLPipeline.Interact import InteractionDefiner
#Standardizer

dl = DataLoader(os.path.join(sys.path[0],'Data'),'training.csv','test.csv')

train_data, test_data = dl.load()
train_data.name = 'train_data'
test_data.name = 'test_data'


#Imp = VarImputer()
#Imp.imp_define(train_data, ['Trim'], output='impute_definitions.csv')
#train_data = Imp.imp_apply(train_data,input='impute_definitions.csv')

#train['mean_MMRAcquisitionAuctionAveragePrice_Make']=train.groupby(['Make'])['MMRAcquisitionAuctionAveragePrice'].transform('mean')
Intr = InteractionDefiner()
Intr.define_rank_interactor(train_data,['MMRAcquisitionAuctionAveragePrice','MMRAcquisitonRetailCleanPrice'], ['Make','Color'],'rank_interact_definitions.csv')
Intr.calculate(train_data,'rank_interact_definitions.csv')
Intr.calculate(test_data,'rank_interact_definitions.csv')
