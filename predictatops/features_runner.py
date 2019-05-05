# -*- coding: utf-8 -*-
################ imports ###################
import pandas as pd
################ import from other python files in this package ###################
from features import *
from configurationplusfiles_runner import input_data_inst, config, output_data_inst


#########################################
################ code ###################


################ Load dataframe from wellKNN script ###################

# path_to_prev_results = output_data_inst.base_path_for_all_results
# path_to_directory = output_data_inst.path_wellKNN
# file_name = output_data_inst.wellsKNN_results_wells_df
# ending = output_data_inst.default_results_file_format

# full_path_to_results_file_from_last_step = getMainDFsavedInStep(path_to_prev_results,path_to_directory,file_name,ending)

# wells_df_from_wellsKNN  = pd.read_hdf(full_path_to_wellsKNN_results)

#### full thing in one step
wells_df_from_wellsKNN = get_wellsKNN_results(output_data_inst)
print("columns",wells_df_from_wellsKNN.columns)
print("len(wells_df_from_wellsKNN 1)",len(wells_df_from_wellsKNN))

################ Load wells df saved from running split functions ###################
################ This file is wells loaded with no features but does have a column for train test split ###################
##### path to input file ######



# split_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_split
# split_file = output_data_inst.split_results_wells_df
# ending = output_data_inst.default_results_file_format
# full_path_to_split_results = split_dir+"/"+split_file+ending
# ##### loading wells df created in split ######
# wells_df_from_split  = pd.read_hdf(full_path_to_split_results)

# print("wells_df_from_split.columns",wells_df_from_split.columns)

wells_df_from_split_curveData = get_split_curve_results(output_data_inst)
print("len(wells_df_from_split_curveData)",len(wells_df_from_split_curveData))
print("wells_df_from_split_curveData.columns",wells_df_from_split_curveData.columns)


    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################
    ####### THIS IS THE PART THAT ISN"T WORKING ################

wells_df_from_wellsKNN = convertSiteIDListToUWIList(input_data_inst,wells_df_from_wellsKNN)
print("wells_df_from_wellsKNN",wells_df_from_wellsKNN)

df_all_wells_wKNN = mergeCurvesAndTopsDF(wells_df_from_split_curveData,wells_df_from_wellsKNN,config)
print("len(df_all_wells_wKNN 2)",len(df_all_wells_wKNN))
print("df_all_wells_wKNN.columns",df_all_wells_wKNN.columns)

print("df_all_wells_wKNN.columns",df_all_wells_wKNN.columns)


#### After joining on the nearest neighbor dataframe, we can cast the original columns to floats instead of strings which some but not necessarily all might be.
#### When we do this, be careful about variation in depth column name and rename DEPTH and DEPT to DEPTH

df_all_wells_wKNN = convertAllColButGivenToFloat(config,df_all_wells_wKNN)

df_all_wells_wKNN = takeLASOffUWI(df_all_wells_wKNN,config)
print("df_all_wells_wKNN.info()",df_all_wells_wKNN.info())
# print("number of columns in len(df_all_wells_wKNN.columns)",len(df_all_wells_wKNN.columns))
# print(df_all_wells_wKNN[0:2])

df_all_wells_wKNN_wEdgesMarked = createDepthRelToKnownTopInSameWell(df_all_wells_wKNN)

df_all_wells_wKNN_wEdgesMarked = createFeat_withinZoneOfKnownPick(df_all_wells_wKNN_wEdgesMarked,config)

df_all_wells_wKNN_wEdgesMarked = NN1_TopMcMDepth_Abs(df_all_wells_wKNN_wEdgesMarked,config)

df_all_wells_wKNN_wEdgesMarked = markingEdgeOfWells(df_all_wells_wKNN_wEdgesMarked,config)

print("df_all_wells_wKNN_wEdgesMarked.head()",df_all_wells_wKNN_wEdgesMarked.head())


##################### WINDOWS FEATURES ####################
#### NOTE: There may be a window that pops up and asks you to approve incoming network communication to python3 from Dask.
df_features_result = createManyFeatFromCurvesOverWindows(df_all_wells_wKNN_wEdgesMarked,config)

##################### Save dataframe as hdf #####################
load_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_features
load_filename = output_data_inst.features_results_wells_df+output_data_inst.default_results_file_format
load_results_full_file_path = load_dir+"/"+load_filename

df_features_result.to_hdf(load_results_full_file_path, key='df', mode='w')