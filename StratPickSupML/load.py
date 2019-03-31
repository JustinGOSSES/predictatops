import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
%matplotlib inline
import welly
from welly import Well
import lasio
import glob
from sklearn import neighbors
import math
import dask
import dask.dataframe as dd
from dask.distributed import Client
from dask import delayed
from dask import compute
import dask.dataframe as dd
from dask.distributed import Client


def makeDF(well_list):
    """
    Changes format of well list into a pandas dataframe with one column called "UWI_file".
    """
    formatted_well_list = []
    for eachW in well_list:
        formatted_well_list.append({"UWI_file":eachW})
    wells_df = pd.DataFrame(formatted_well_list)
    return wells_df


def find_number_well_files_in_a_folder(path_to_wells,file_ending):
    """
    Takes in:
    Returns: 
    """
    path_to_all_wells = file_ending+"*"+file_ending
    count = 0
    for file in glob.glob(path_to_all_wells):
        count += 1
    return count

def load_all_wells_in(wells_df,max_numb_wells,path_to_wells,file_ending):
    #### NOTE: limiting wells being read-in to a max number of wells here !!!!!!!!!!!!!!!!
    print("note: the loadAndNoFeatures function in load.py does a data transformation to the UWI that may not be applicable to your dataset!")
    count_limit = max_numb_wells
    count=0
    list_of_failed_wells = []
    ### dictionary that holds every well as key:value or "UWI":df pair
    df_w_dict ={}
    number_of_las = 0
    for file in glob.glob(path_to_wells+"*"+file_ending):
        number_of_las += 1
        count+=1
        if count > count_limit:
            print("hit limit of count below file for loop, count is =",count)
            answer = [df_w_dict,list_of_failed_wells]
            return answer
        else:
            #### Load each well as a pandas dataframe using LASIO, delay compute for parallalism using dask delayed
            l_df = delayed(lasio.read)(file).df()
            # str_uwi= file[-23:-4].replace("-", "/",1)[:17]+file[-6:-4].replace("-", "/",1)
            str_uwi = file[-23:-4][:17]+file[-6:-4]+file_ending
            if any(wells_df.UWI_file == str_uwi):
                l_df = l_df.reset_index()
                df_w_dict[str_uwi]= l_df
            else:
                list_of_failed_wells.append(str_uwi)
                print("could not find UWI match for the well, and well is ",str_uwi,file)            
    l_df = l_df.compute()
    answer = [df_w_dict,list_of_failed_wells]
    print("number of las files=",number_of_las," and number of count=",count)
    return answer



def turn_dict_of_well_dfs_to_single_df(dictOfWellDf):
    """
    Takes in a dict of dataframes, where each dataframe is for a well created by LASIO
    and returns a single dataframe of all wells
    """
    # start by creating empty dataframe and list
    data_df = pd.DataFrame()
    list_of_df = []
    keys = list(dictOfWellDf.keys())
    # get dict of well data frames into values format
    values = dictOfWellDf.values()
    # go through each item in values and add to a list
    count = 0
    for each in values:
        each['UWI'] = keys[count]
        count += 1
        list_of_df.append(each)
    # concat the list into a single dataframe
    data_df = pd.concat(list_of_df)
    return data_df