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
from sklearn.externals import joblib
import multiprocessing
#### Adding this bit to silence an error that was causing the notebook to have a dead kernal
#### This is an unsafe solution but couldn't get any  of the "right solutions" to work!
#### Ended up using this = https://www.kaggle.com/c/bosch-production-line-performance/discussion/25082
#### Other solutions = https://github.com/dmlc/xgboost/issues/1715 but the solution here didn't seem to work for me?
import os
#os.environ['KMP_DUPLICATE_LIB_OK']='True'

######## Input variables defined at start   @###########


def findDirAndPathForBalancedresults():

    return 

class ML_obj_class():
    """doc string"""
    ##def __init__(self, knn_dir,load_dir,features_dir,machine_learning_dir,h5_to_load ):
    def __init__(self, output_data_inst):
        # self.knn_dir = knn_dir
        # self.load_dir = load_dir
        # self.features_dir = features_dir
        self.machine_learning_dir = output_data_inst.base_path_for_all_results +"/"+ output_data_inst.path_balance
        self.h5_to_load = output_data_inst.balance_results_wells_df + output_data_inst.default_results_file_format
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
    
    def dropCol(self,df,col_list):
        """doc string goes here"""
        df = df.drop(columns=col_list)
        return df
    
    def dropNeighbors_ObjCol(self,col_list):
        """doc string goes here"""
        try:
            self.train_X = self.dropCol(self.train_X,col_list)
            self.test_X = self.dropCol(self.test_X,col_list)
            self.preSplitpreBal = self.dropCol(self.preSplitpreBal,col_list)
            print("dropped :",col_list," in train_X, test_X, and preSplitpreBal dataframes")
        except:
            print("Could not find something in ",col_list," and such did not drop :",col_list," in train_X, test_X, and preSplitpreBal dataframes. It may nto exist.")
        
    def load_data_for_ml(self):
        """
        doc string goes here
        """
        self.train_X = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'train_X')
        self.train_y = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'train_y')
        self.test_X = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'test_X')
        self.test_y = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'test_y')
        self.train_index = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'train_index')
        self.test_index = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'test_index')
        self.preSplitpreBal = pd.read_hdf(self.machine_learning_dir+"/"+self.h5_to_load, 'preSplitpreBal')
        #print("X and Y in the test dataset should be the same size", " test_X = ",len(self.test_X)," and test_y =",len(self.test_y)," and test_index=",len(self.test_index))
        check_response_test = self.check_test_df_same_size()
        check_response_train = self.check_train_df_same_size()
        print(check_response_test)
        print(check_response_train)
        return "Loading the h5 format data into pandas finished. You may access the dataframes by appending to the ML1 object .train_X | .train_y | test_X | .test_y | .train_index | .test_index | .preSplitpreBal"
    
    def init_XGBoost_withSettings(self):
        """
        Takes in 
        Returns
        """
        
        ##########################     Initial Machine Learning Using XGBoost classification   ##########################
        ##########################     Optional
        model = XGBClassifier(
            max_depth=3,
            objective='multi:softmax',  # error evaluation for multiclass training
            num_class=5,
            n_gpus= 0,
            n_jobs=-1
            # gamma=gamma, 
            # reg_alpha=reg_alpha, 
            # max_depth=max_depth, 
            # subsample=subsample, 
            # colsample_bytree= colsample_bytree, 
            # n_estimators= n_estimators, 
            # learning_rate= learning_rate, 
            # min_child_weight= min_child_weight,
            # n_jobs=n_jobs
            #params
        )
        print(" init_XGBoost_withSettings function has been called which initiates a XGBoost classifier with settings of : max_depth=4,objective='multi:softmax', training,num_class=5,n_gpus= 0,n_jobs=8")
        print("model coming out of init_XGBoost_withSettings() function is:",model)
        return model
                            

def saveTrainClassesResultsAsPickle(model,MLinstance,output_data_inst):
    """
    Takes in 
    Saves 
    Returns 
    NOTE: This pickle may have problems loading properly if you switch OS or version of Python!!!
    """
    ###### Establish file path to save 
    load_dir = output_data_inst.base_path_for_all_results + "/" + output_data_inst.path_trainclasses
    load_results_full_file_path = load_dir+"/"+output_data_inst.trainclasses_results_model+output_data_inst.default_results_file_format
    #########################  Write each pandas dataframes to single HDF5 using separate keys to retrieve later
    # Save to file in the current working directory
    joblib_file = "trainclasses_model.pkl"  
    joblib_file = load_dir+"/"+joblib_file 
    joblib.dump(model, joblib_file)
    #model.to_hdf(load_results_full_file_path, key='model', mode='w')
    joblib_fileMLInstance = load_dir+"/"+"trainclasses_ML1_instance.pkl"
    joblib.dump(MLinstance, joblib_fileMLInstance)
    print("finished saving the results of the model step in the location set in the output class instance. = ",joblib_file)

