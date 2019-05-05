# -*- coding: utf-8 -*-


################ imports ###################
import pandas as pd
import numpy as np
import itertools
# import matplotlib.pyplot as plt
# %matplotlib inline
import welly
from welly import Well
import lasio
import glob
from sklearn import neighbors
import pickle
import math
import dask
import dask.dataframe as dd
from dask.distributed import Client
import random
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import multiprocessing
#### Adding this bit to silence an error that was causing the notebook to have a dead kernal
#### This is an unsafe solution but couldn't get any  of the "right solutions" to work!
#### Ended up using this = https://www.kaggle.com/c/bosch-production-line-performance/discussion/25082
#### Other solutions = https://github.com/dmlc/xgboost/issues/1715 but the solution here didn't seem to work for me?
import os
#os.environ['KMP_DUPLICATE_LIB_OK']='True'

######## Input variables defined at start   @###########

class ML_obj_class():
    """doc string"""
    def __init__(self, knn_dir,load_dir,features_dir,machine_learning_dir,h5_to_load ):
        self.knn_dir = knn_dir
        self.load_dir = load_dir
        self.features_dir = features_dir
        self.machine_learning_dir = machine_learning_dir
        self.h5_to_load = h5_to_load 
        self.train_X = None
        self.train_y = None
        self.test_X = None
        self.test_y = None
        self.train_index = None
        self.test_index = None
        self.preSplitpreBal = None
        
    def check_test_df_same_size(self):
        """doc string goes here"""
        if len(self.test_X) == len(self.test_y) and len(self.test_y)==len(self.test_index):
            response = "PASSED: test_X and test_y and test_index are all the same size as asserted "+str(len(self.test_X))
        else:
            response = "FAIL?: test_X and test_y in the test dataset should be the same size BUT THEY ARE NOT!!! test_X = "+str(len(self.test_X))+" and test_y ="+str(len(self.test_y))+" and test_index="+str(len(self.test_index))
        return response
    
    def check_train_df_same_size(self):
        """doc string goes here"""
        if len(self.train_X) == len(self.train_y) and len(self.train_y)==len(self.train_index):
            response = "PASSED: train_X and train_y and train_index are all the same size as asserted "+str(len(self.train_X))
        else:
            response = "FAIL?: train_X and train_y and train_index should be the same size BUT THEY ARE NOT!!! train_X = "+str(len(self.train_X))+" and train_y ="+str(len(self.train_y))+" and train_index="+str(len(self.train_index))
        return response
        
    def load_data_for_ml(self):
        """
        doc string goes here
        """
        self.train_X = pd.read_hdf(self.machine_learning_dir+self.h5_to_load, 'train_X')
        self.train_y = pd.read_hdf(self.machine_learning_dir+self.h5_to_load, 'train_y')
        self.test_X = pd.read_hdf(self.machine_learning_dir+self.h5_to_load, 'test_X')
        self.test_y = pd.read_hdf(self.machine_learning_dir+self.h5_to_load, 'test_y')
        self.train_index = pd.read_hdf(self.machine_learning_dir+self.h5_to_load, 'train_index')
        self.test_index = pd.read_hdf(self.machine_learning_dir+self.h5_to_load, 'test_index')
        self.preSplitpreBal = pd.read_hdf(machine_learning_dir+h5_to_load, 'preSplitpreBal')
        #print("X and Y in the test dataset should be the same size", " test_X = ",len(self.test_X)," and test_y =",len(self.test_y)," and test_index=",len(self.test_index))
        check_response_test = self.check_test_df_same_size()
        check_response_train = self.check_train_df_same_size()
        print(check_response_test)
        print(check_response_train)
        return "Loading the h5 format data into pandas finished. You may access the dataframes by appending to the ML1 object .train_X | .train_y | test_X | .test_y | .train_index | .test_index | .preSplitpreBal"
    def init_XGBoost_withSettings(self):
        """
        doc string
        uses settings from previous test on manville dataset
        Use your own once you can optmize the settings
        """
        print("model = XGBClassifier(gamma=0, reg_alpha=0.3, max_depth=6, subsample=0.8, colsample_bytree= 0.8, n_estimators= 300, learning_rate= 0.03, min_child_weight= 3,n_jobs=8)")
        model = XGBClassifier(
            gamma=0, 
            reg_alpha=0.3, 
            max_depth=6, 
            subsample=0.8, 
            colsample_bytree= 0.8, 
            n_estimators= 300, 
            learning_rate= 0.03, 
            min_child_weight= 3,n_jobs=8)
        return model
                            