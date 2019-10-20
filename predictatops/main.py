# -*- coding: utf-8 -*-
"""
    The main.py module of predictatops merely holds a few utility functions leveraged by other modules.
"""

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
    """
    This function simply prints a hello message for testing.
    """
    print("hello, you've run the main module")


def load_prev_results_at_path(full_path_to_results_file, key="df"):
    """
    A function used to return a dataframe of wells stored in an h5 file at a given path with a given key.
    
    Parameters
    ----------
    full_path_to_results_file: string
        A path to a .h5 file that contains a wells dataframe.

    key: string
        A string representation of a key used to find the dataframe in the h5 file whose path is defined by the full_path_to_results_file argument.

    Returns
    -------
    wells_df_from_wellsKNN: dataframe
        Returns a dataframe of wells that existed at the path defined in the full_path_to_results_file argument.
    """
    wells_df_from_wellsKNN = pd.read_hdf(full_path_to_results_file, key=key)
    return wells_df_from_wellsKNN


def getMainDFsavedInStep(path_to_results, path_to_directory, file_name, ending):
    """
    A function used to return a dataframe of data stored in a file at a given path. Not specific to a dataframe of wells in h5 file like load_prev_results_at_path.
    
    Parameters
    ----------
    path_to_results: string
        A path to a top-level results folder.

    path_to_directory: string
        A path to a folder within the results folder that has the file in question.

    file_name: string
        A path to a file within the path_to_results and path_to_directory arguments.
    
    ending: string
        String representation of the file type like ".h5" or ".csv". It should include the dot!

    Returns
    -------
    full_path_to_results_file: string
        Returns a string representation of the full path to the file in question.

    """
    dir_path = path_to_results + "/" + path_to_directory
    full_path_to_results_file = dir_path + "/" + file_name + ending
    return full_path_to_results_file


def get_df_results_from_step_X(output_data_inst, directory, filename, key="df"):
    """
    Another function used to return a dataframe stored in an h5 file at a given path with a given key.
    
    Parameters
    ----------
    output_data_inst: string
        A path to a folder with previously output data.

    directory: string
        A folder within the directory defined by the 'output_data_inst' that holds a file.

    key: string
        A string representation of a key used to find the dataframe in the h5 file. Default is "df".

    Returns
    -------
    wells_df_of_results: dataframe
        Returns a dataframe of wells that existed at the path defined via the given input arguments.
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
    Another function used to generate the string representation of the path to a pickle file and then returns that pickled datafile.
    
    Parameters
    ----------
    output_data_inst: string
        A path to a folder with previously output data.

    subfolder: string
        A folder within the directory defined by the 'output_data_inst' that holds a file.

    filename: string
        Name of the file in question.

    Returns
    -------
    joblib.load(full_path_to_pickle): dataframe
        Returns a dataframe that exists at the path defined via the given input arguments.
    """
    full_path_to_pickle = (
        output_data_inst.base_path_for_all_results + "/" + subfolder + "/" + filename
    )
    return joblib.load(full_path_to_pickle)
