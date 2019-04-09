# -*- coding: utf-8 -*-

##### import statements #####
import pandas as pd
import numpy as np
import itertools
# import matplotlib.pyplot as plt
# %matplotlib inline
import welly
from welly import Well
import lasio
import glob
import math
#### Dask is used here to slightly improve speed of loading. This needs further refined to work well but kept in for now.
import dask
import dask.dataframe as dd
from dask.distributed import Client
from dask import delayed
from dask import compute
import dask.dataframe as dd
from dask.distributed import Client



##### Classes #####
##### none


##### Functions not in class objects
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
    Takes in: a path to a directory and a file ending we're searching for
    Returns: the number  of files in that directory withe that file ending
    """
    path_to_all_wells = path_to_wells+"*"+file_ending
    count = 0
    for file in glob.glob(path_to_all_wells):
        count += 1
    return count

def load_all_wells_in(wells_df,max_numb_wells,path_to_wells,file_ending):
    """
    Takes in: a dataframe of well names called wells_df, the max number of wells if we're doing testing and don't want to bother with all the wells, path to directory with well files, and file ending for well files, like .LAS.
    Returns: A list with two dicts. One of successfully imported wells, the other with wells that failed to import for various reasons. This then further processed by turn_dict_of_well_dfs_to_single_df() in the next step.
    """

    #### NOTE: limiting wells being read-in to a max number of wells here !!!!!!!!!!!!!!!!
    print("note: the loadAndNoFeatures function in load.py does a data transformation to the UWI that may not be applicable to your dataset!")
    # print("example well UWI",wells_df["UWI_file"][0])
    print("example ,wells_df",wells_df)
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
            #l_df = delayed(lasio.read)(file).df()
            l_df = lasio.read(file).df()
            # str_uwi= file[-23:-4].replace("-", "/",1)[:17]+file[-6:-4].replace("-", "/",1)
            file = file.replace(path_to_wells,"")
            str_uwi = file[-23:-4][:17]+file[-6:-4]+file_ending
            
            print(str_uwi, "is str_uwi and ",wells_df.wells[0], "is a wells_df.UWI_file[0]")
            #if str(str_uwi) isin wells_df.wells:
            if any(wells_df.wells == str_uwi):
                l_df = l_df.reset_index()
                df_w_dict[str_uwi]= l_df
            else:
                
                list_of_failed_wells.append(str_uwi)
                #print("could not find UWI match for the well, and well is ",str_uwi,file)            
    #l_df = l_df.compute()
    answer = [df_w_dict,list_of_failed_wells]
    print("number of las files=",number_of_las," and number of count=",count)
    print("number of read wells",len(df_w_dict)," number of wells not read as they don't have needed tops or curves or could not be read is ",len(list_of_failed_wells))
    return answer



def turn_dict_of_well_dfs_to_single_df(dictOfWellDf):
    """
    Takes in a dict of dataframes, where each dataframe is for a well created by LASIO. Likely created by load_all_wells_in function and is the first item in the returned list.
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