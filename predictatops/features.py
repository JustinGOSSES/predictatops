# -*- coding: utf-8 -*-

##### import statements #####
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
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
# import pdvega
# import vega
#from IPython.display import display
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.options.display.max_colwidth = 100000



################### Purpose for this code ###################
#### Feature Creation
####
###################################################################



################ Load dataframe of tops data from wellKNN script ###################

def getMainDFsavedInStep(path_to_results,path_to_directory,file_name,ending):
    """
    Takes in 
    Returns
    """
    dir_path = path_to_results + "/" + path_to_directory
    full_path_to_results_file = dir_path+"/"+file_name+ending
    return full_path_to_results_file

def load_prev_results_at_path(full_path_to_results_file):
    """
    Takes in 
    Returns
    """
    wells_df_from_wellsKNN  = pd.read_hdf(full_path_to_results_file)
    return wells_df_from_wellsKNN

def get_wellsKNN_results(output_data_inst):
    """
    Takes in 
    Returns
    """
    #### get parts of the path to the resulting dataframe from wellsKN from the output_data_inst variable
    path_to_prev_results = output_data_inst.base_path_for_all_results
    path_to_directory = output_data_inst.path_wellKNN
    file_name = output_data_inst.wellsKNN_results_wells_df
    ending = output_data_inst.default_results_file_format
    ##### combine all those variables into a single 

    full_path_to_wellsKNN_results = getMainDFsavedInStep(path_to_prev_results,path_to_directory,file_name,ending)
    ##### load dataframe from full path
    wells_df_from_wellsKNN  = load_prev_results_at_path(full_path_to_wellsKNN_results)
    return wells_df_from_wellsKNN


################ Load dataframe with curve data from split script ###################
def get_split_curve_results(output_data_inst):
    """
    Takes in 
    Returns
    """
    #### get parts of the path to the resulting dataframe from wellsKN from the output_data_inst variable
    path_to_prev_results = output_data_inst.base_path_for_all_results
    path_to_directory = output_data_inst.path_split
    file_name = output_data_inst.split_results_wells_df
    ending = output_data_inst.default_results_file_format
    ##### combine all those variables into a single 

    full_path_to_split_curve_results = getMainDFsavedInStep(path_to_prev_results,path_to_directory,file_name,ending)
    ##### load dataframe from full path
    wells_df_from_split_curveData  = load_prev_results_at_path(full_path_to_split_curve_results)
    return wells_df_from_split_curveData


def mergeCurvesAndTopsDF(wells_df_from_split_curveData,wells_df_from_wellsKNN,config):
    """
    Takes in 
    Returns
    """
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    
    df_all_wells_wKNN = pd.merge(wells_df_from_split_curveData, wells_df_from_wellsKNN, on=config.UWI)
    return df_all_wells_wKNN

#####################

def convertAllColButGivenToFloat(config,df_all_wells_wKNN):
    """
    Takes in 
    Returns
    """
    #keepStringsArray = ['UWI', 'SiteID', 'trainOrTest','Neighbors_Obj']
    keepStringsArray = config.colsToNotTurnToFloats
    print("turning all columns but these into floats. Should come from config.colsToNotTurnToFloats",keepStringsArray)
    columns = list(df_all_wells_wKNN.columns.values)
    columns_to_turn_to_floats = [item for item in columns if item not in keepStringsArray]
    df_all_wells_wKNN = df_all_wells_wKNN[columns_to_turn_to_floats].astype(float)
    return df_all_wells_wKNN