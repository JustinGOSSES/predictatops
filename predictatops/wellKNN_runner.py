# -*- coding: utf-8 -*-
################ imports ###################
import pandas as pd
################ import from other python files in this package ###################
from wellsKNN import *
from configurationplusfiles_runner import input_data_inst, config, output_data_inst



################ Load wells df saved from running split functions ###################
################ This file is wells loaded with no features but does have a column for train test split ###################
##### path to input file ######
split_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_split
split_file = output_data_inst.split_results_wells_df
ending = output_data_inst.default_results_file_format
full_path_to_split_results = split_dir+"/"+split_file+ending
##### loading wells df created in split ######
wells_df_from_split  = pd.read_hdf(full_path_to_split_results)
#print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH",wells_df_from_split.columns)


################ Load all df for picks, pick dictionary, wells, and coordinate data. ###################
################ Paths for loading these come from input_data class in configurationplusfiles.py ###################
picks, picks_dic, wells, gis  = get_data_for_wellsKNN(input_data_inst)

################ Target is the name of the top we're trying to predict ###################
################ target_base is the name of the top under if we're using for guidance ###################
target, target_base = getTopsForWantedPickNames(config)


################ Generates two dataframes. Each with the pick depths of only a given top. ###################
picks_targetTop, picks_targetBase = findAllPicksForTops(picks, target, target_base, config.HorID_name_col_in_picks_df)

################ Merges many of the dataframes together based on config.siteID_col_in_picks_df ###################
df_new = mergeDataframes(wells,picks_targetTop,config.siteID_col_in_picks_df,picks_targetBase, gis)

print(df_new.head())

################ Let's limit the GIS and pick information dataframe to only the wells we're going to use and ###################
################ exclude any we're not going to use for not having the needed tops and curves. ###################
################ We'll have to change the format of the UWU col slightly to do this ###################

wellsLoaded_list = createListOfWellNamesLoadedSplit(wells_df_from_split,config)


new_wells_loaded_list_inUWIstyle = findListOfConvertedUWInamesForWellsLoaded(wells_df_from_split,config.UWI,input_data_inst.well_format)
print("new_wells_loaded_list_inUWIstyle[5:8]",new_wells_loaded_list_inUWIstyle[5:8])

################ This next step will reduce the total number of wells to just the ones that have at least the tops and curves we need ################ 

df_reduced = reduced_df_from_split_plus_more(df_new,new_wells_loaded_list_inUWIstyle,config.UWI)

################ We'll now find nearest N neighbors using a kdtree approach ################ 
tree, dist, ind = kdtree(df_reduced, input_data_inst.gis_lat_col, input_data_inst.gis_long_col, config.kdtree_leaf, config.kdtree_k)


UWIs_Geog = makeKNearNeighObj(df_reduced,config.UWI,input_data_inst.gis_lat_col, input_data_inst.gis_long_col,dist,ind,config.kdtree_k)
print("UWIs_Geog.head()",UWIs_Geog.head())

################# Now to clean the dataframe, rename columns, and merge with the new dataframe that has the neighbors! ##################
df_new_cleaned = cleanRenameDF(df_reduced,target, target_base,config,input_data_inst)

print("type df_new_cleaned",type(df_new_cleaned))
print(df_new_cleaned)
print("df_new_cleaned.head()",df_new_cleaned.head())

df_new_cleaned_plus_nn = mergeCleanedAndUWIGeog_dfs(df_new_cleaned,UWIs_Geog)

print("This is how to access the data on nearest neigbhors in the 'Neighbors_Obj' column - df_new_cleaned_plus_nn.loc[1:1,'Neighbors_Obj'][1][1] =",df_new_cleaned_plus_nn.loc[1:1,'Neighbors_Obj'][1][1])

print("an example of neighbors is : df_new_cleaned_plus_nn.loc[1:2,'Neighbors_Obj'][2] which is = ",df_new_cleaned_plus_nn.loc[1:2,'Neighbors_Obj'][2])

################# 6 and 7 in the functions below are the 6th and 7th columns... should replace with something more obvious!!!!! ##################
df_new_cleaned_plus_nn_temp = broadcastFuncForFindNearestNPickDepth(df_new_cleaned_plus_nn, 7, config.NN1_topTarget_DEPTH, config.UWI)
df_new2 = broadcastFuncForFindNearestNPickDepth(df_new_cleaned_plus_nn_temp, 6, config.NN1_TopHelper_DEPTH, config.UWI)


df_new3 = useThicknessOfNeighborsToEst(df_new2)

print("printing first row of df_new2 in wellKNN_runner.py",df_new3[0:1])


df_new3 = create_diff_Top_Depth_Real_v_predBy_NN1thick(df_new3)

######
######
###### df_new3 has both train and test. That is find for finding neighbors for test wells, but
###### for train wells we should only be including information from other train wells. 
###### it would not be fair to include test well neihbor information in training data!!!
###### We'll redo the steps above now but just for training wells. 
###### Firs though, we'll take what we've build and slice off just the test wells into a new dataframe.

df_completed_test = getTestRowsOnlyPicksDF(df_new3,wells_df_from_split,config,"test",input_data_inst.well_format)


#df_completed_test = onlyWellsInTestPortion(df_new3,"test")

#### okay now lets run the whole thing with just the train wells

df_train = onlyWellsInTestPortion(wells_df_from_split,"train")

df_nearly_completed_train = fullWellsKNN(df_train,input_data_inst,config)
print("len(df_nearly_completed_train)",len(df_nearly_completed_train))
df_completed_train = getTestRowsOnlyPicksDF(df_nearly_completed_train,df_train,config,"train",input_data_inst.well_format)
print("len(df_completed_test) =",len(df_completed_test))
print("len(df_completed_train)",len(df_completed_train))

df_completed_trainAndTest = pd.concat([df_completed_train, df_completed_test])
print("length df_completed_trainAndTest = ",len(df_completed_trainAndTest))

#### Save dataframe as hdf

load_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_wellKNN
load_filename = output_data_inst.wellsKNN_results_wells_df+output_data_inst.default_results_file_format
load_results_full_file_path = load_dir+"/"+load_filename

df_completed_trainAndTest.to_hdf(load_results_full_file_path, key='df', mode='w')