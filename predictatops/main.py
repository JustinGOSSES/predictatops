# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt

# %matplotlib inline
import welly
from welly import Well
import lasio
import glob
from sklearn.externals import joblib

### """Main module."""


def printHello():
    print("hello, you've run the main module")


def load_prev_results_at_path(full_path_to_results_file, key="df"):
    """
    Takes in 
    Returns
    """
    wells_df_from_wellsKNN = pd.read_hdf(full_path_to_results_file, key=key)
    return wells_df_from_wellsKNN


def getMainDFsavedInStep(path_to_results, path_to_directory, file_name, ending):
    """
    Takes in 
    Returns
    """
    dir_path = path_to_results + "/" + path_to_directory
    full_path_to_results_file = dir_path + "/" + file_name + ending
    return full_path_to_results_file


def get_df_results_from_step_X(output_data_inst, directory, filename, key="df"):
    """
    Takes in 
    Returns
    """
    #### get parts of the path to the resulting dataframe from wellsKN from the output_data_inst variable
    ending = output_data_inst.default_results_file_format
    base_path_for_all_results = output_data_inst.base_path_for_all_results
    ##### combine all those variables into a single
    full_path_to_features_results = getMainDFsavedInStep(
        base_path_for_all_results, directory, filename, ending
    )
    ##### load dataframe from full path
    wells_df_of_results = load_prev_results_at_path(full_path_to_features_results, key)
    return wells_df_of_results


def getJobLibPickleResults(output_data_inst, subfolder, filename):
    """
    Inputs
    Returns
    """
    full_path_to_pickle = (
        output_data_inst.base_path_for_all_results + "/" + subfolder + "/" + filename
    )
    return joblib.load(full_path_to_pickle)
