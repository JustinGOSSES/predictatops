# -*- coding: utf-8 -*-

##### import statements #####
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
#%matplotlib inline
import welly
from welly import Well
import lasio
import glob
from sklearn import neighbors
import os
import folium
#print("folium",folium.__version__)
import branca.colormap as cm
import os
import math
#print("welly",welly.__version__)
import re


################### Purpose for this code ###################
# Purpose of this notebook = leverage knowledge about neighbors formation thicknesses & nearby well depths
# What a geologist would do:
# Look at neighboring wells to find thickness of unit from a top and base pick, in prediction well flatten on base pick, and see where neighboring top pick lands on well in question. Further evaluation starts there.
# Feature creation summary:
# Find thickness of unit in neighboring wells in training dataset. Subtract that thickness from the base pick depth in the well we're going to predict for to find where that top pick would be in the prediction well if the thickness is the same.
# Feature Creation Additional Details:

#     We could get quite elaborate with this in terms of whether neighbors are on all sides of prediction well or just one side or which neighbors are most similar in terms of total depth drilled, variances in gamma-ray, etc.
#     For now, we're going going to create two features (1) a prediction feature based on nearest neighbor thickness (2) a prediction feature based on average of nearest 5 neighbors.
#     Neighbor thickness helper features columns will be floats representing the distance from the depth predicted from neighbor thickness and prediction well base pick.
#     We will also have column to keep track of the range between the smallest and largest neighbor thickness of that well.
#     This feature creation requires the things below, if they aren't present this shouldn't be used:
#         We have lat/long to determine neighbors.
#         We have a base pick and a top pick for each well.
#         We have reason to believe the thickness of neighbors is a good indicator or where the top will be in this well. Reasons that wouldn't be the case include: presence of faults, known local outliers, and possibly other things I haven't thought of yet.
##############################################################


################ Load all df for picks, pick dictionary, wells, and coordinate data. ###################
################ Paths for loading these come from input_data class in configurationplusfiles.py ###################
def get_data_for_wellsKNN(input_data_inst):
    """
    Takes in a class instance of the input data class which has information on the paths needed to load various dataframe of data
    Returns dataframes of picks, pick dictionaries, well names, and gis data.
    """
    picks = input_data_inst.picks_df
    picks_dic = pd.read_csv(input_data_inst.picks_dic,input_data_inst.picks_dic_file_path_delimiter)
    input_data_inst.load_wells_file()
    wells = input_data_inst.wells_df
    gis = input_data_inst.load_gis_file()

    return picks, picks_dic, wells, gis 


##### Give top pick code that we want to predict and give base pick code that we want to assume we have #####
# ##### Dataframe of well curves data created in load notebook #####
# #### top pick code we are going to predict
# picks_targetTop=picks[picks['HorID']==13000]
# #### base pick code we are going to assume we have
# picks_targetBase=picks[picks['HorID']==14000]

def getTopsForWantedPickNames(config):
    """
    Takes in: configuration instance object
    Returns: two strings or integers that are the target top and top below target top
    """
    target = config.target_top
    target_base = config.top_under_target
    return target, target_base

################ Get pick dataframes with just specific tops ###################
def findAllPicksForTops(picks, target, target_base, HorID):
    """
    Takes in: picks dataframe, target top string, top under top target, and string for HorID column name.
    Returns: 2 dataframes, first with only pick depths for target top, and second with pick depths for only top under target top.
    """
    #### top pick code we are going to predict
    picks_targetTop=picks[picks[HorID] == target]
    #### base pick code we are going to assume we have
    picks_targetBase=picks[picks[HorID] == target_base]
    return picks_targetTop, picks_targetBase



def mergeDataframes(wells,picks_targetTop,SitID,picks_targetBase, gis):
    """
    Takes in:
    Returns: 
    """
    df_new = pd.merge(wells, picks_targetTop, on='SitID')
    df_paleoz = pd.merge(wells, picks_targetBase, on='SitID')
    df_gis = pd.merge(df_paleoz, gis, on='SitID')
    df_new=pd.merge(df_gis, df_new, on='SitID')
    df_new.head()
    return df_new



################ Functions for limiting the df_new dataframe to only those wells loaded in load step. ###################
################ This will involve changes to the well name as there are `/` in the name when in a file #################
################ but those are changed to `-` in filenames. ###################

def createListOfWellNamesLoadedSplit(wells_df_from_split,config):
    wellsLoaded_list = wells_df_from_split[[config.UWI]][config.UWI].unique()
    len(wellsLoaded_list)
    print("examples of what the well format looks like in wellsLoaded_list",wellsLoaded_list[9:12])
    return wellsLoaded_list

def replacenthSubStr(string, sub, wanted, n):
    """
    Takes in:
    Returns: 
    """
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

def changeLASfileToBeUWIstr(lasStr,well_format_str):
    """
    Takes in:
    Returns: 
    """
    string1 = replacenthSubStr(lasStr,'-', '/', 5)
    string2 = replacenthSubStr(string1,'-', '/', 1).replace(well_format_str,"")
    return string2


def findListOfConvertedUWInamesForWellsLoaded(wellsLoaded_df_fromh5,UWI,well_format_str):
    """
    Takes in:
    Returns: 
    """
    wellsLoaded_list = wellsLoaded_df_fromh5[[UWI]][UWI].unique()
    new_wells_loaded_list_inUWIstyle = []
    for lasStr in wellsLoaded_list:
        new_wells_loaded_list_inUWIstyle.append(changeLASfileToBeUWIstr(lasStr,well_format_str))
    return new_wells_loaded_list_inUWIstyle



################ This next step will reduce the total number of wells to just the ones that have at least the tops and curves we need ################

def reduced_df_from_split_plus_more(df_new,new_wells_loaded_list_inUWIstyle,UWI):
    """
    Takes in:
    Returns: 
    """
    df_new_allWells = df_new.copy()
    print("len(df_new_allWells)",len(df_new_allWells))
    df_reduced = df_new[df_new[UWI].isin(new_wells_loaded_list_inUWIstyle)]
    df_reduced = df_new.reset_index(drop=True)
    ##### Now that we've reduced the wells, we'll reset the index. #####
    ##### We'll do this because another step below will use a loop that gets confused if there are index values missing. #####
    return df_reduced

################ We'll now find nearest N neighbors using a kdtree approach ################ 

def kdtree(df_reduced,lat_col,long_col,leaf_size,k):
    """
    Takes in:
    Returns: 
    """
    position = df_reduced[[lat_col,long_col]]
    tree = neighbors.KDTree(position, leaf_size=leaf_size) 
    dist, ind = tree.query([position][0], k=k)  
    return tree, dist, ind


def makeKNearNeighObj(df_reduced,UWI,Lat,Long,dist,ind,numberNeighbors):
    """
    Takes in:
    Returns: 
    """
    ##### first part......
    #### make a data frame of UWI & index from main dataframe
    UWIs = df_reduced[['UWI']]
    position = df_reduced[['lat','lng']]
    #UWIs.join(position, how='outer') 
    UWIs_Geog = pd.concat([UWIs, position], axis=1)
    #print(UWIs_Geog.head())
    #### Add object of tree for 8 neighbors to a dataframe
    #latlng_kd_tree_leaf2 = pd.read_pickle(pickleFileOfKDtree)
    #### Finding 8 nearest neighbors based on lat/long
    #### K is number of neighbors
    #dist, ind = latlng_kd_tree_leaf2.query([position][0], k=numberNeighbors) 

    neighbor_array_per_well_row = []
    #### for i in ind.length
    for i in range(len(ind)):
        #### get the array of index values of neighbors, note: first one is the point in question which should be ignored!
        neighbors_ind = ind[i][1:]
        # for each index in that array, 
        counter = 1
        array_of_holder_obj = []
        for n in neighbors_ind:
            #### start temp object of {"neighbor":"int","UWI":"string","distance":"float"}
            holder_obj = {"neighbor":"int","UWI":"string","distance":"float"}
            #### get the distance into the temp object using index of i and each,
            holder_obj['distance'] = dist[i][counter]
            #### get the UWI using i and the dataframe
            holder_obj['UWI'] = UWIs_Geog.loc[n,'UWI']
            #### and position via "counter"
            holder_obj['neighbor'] = counter
            #### add the temp object populated as a column entry into an array
            counter = counter + 1
            array_of_holder_obj.append(holder_obj)
        #### turn array of objects into series and add as new column to dataframe
        neighbor_array_per_well_row.append(array_of_holder_obj)
    UWIs_Geog['Neighbors_Obj'] = pd.Series(neighbor_array_per_well_row,index=UWIs.index)
    return UWIs_Geog


def getColNames_for_cleanRenameDF(config):
    """
    Takes in:
    Returns: 
    """
    SitID_col = config.siteID_col_in_picks_df = 'SitID'
    UWI_col = config.UWI = "UWI"
    HorID_col = config.HorID_name_col_in_picks_df = "HorID"
    Quality_col = config.quality_col_name_in_picks_df = "Quality"
    Pick_depth_col = config.picks_depth_col_in_picks_df = 'Pick'
    return SitID_col, UWI_col, HorID_col, Quality_col, Pick_depth_col

def cleanRenameDF(df,topTarget,thicknessHelperTop,config,input_data_inst):
    """
    Takes in:
    Returns: 
    """
    #### HorID and Pick should be for the topTarget & HorID_x and Pick_x should be for helper top which is a base of the unit
    #### First step is to check the assumption above:
    SitID_col, UWI_col, HorID_col, Quality_col, Pick_depth_col = getColNames_for_cleanRenameDF(input_data_inst)
    lat = input_data_inst.gis_lat_col
    lng = input_data_inst.gis_long_col
    if int(df[HorID_col][0:1][0]) != int(topTarget) or int(df[HorID_col+'_x'][0:1][0]) != int(thicknessHelperTop):
        print(df[HorID_col][0:1][0], "should equal topTarget",topTarget)
        print( df[HorID_col][0:1][0], " should also equal, thicknessHelperTop",thicknessHelperTop )
        return "THERE WAS A PROBLEM AND THE COLUMNS AND TOPS VALUES DONT MATCH IN cleanRenameDF"
    else:
        df_new_cleaned = df[[SitID_col,HorID_col+'_x',Pick_depth_col+'_x',Quality_col+'_x',HorID_col,Pick_depth_col,Quality_col,lat,lng,UWI_col]].copy()
        df_new_cleaned['TopHelper_HorID'] = df_new_cleaned[HorID_col+'_x']
        df_new_cleaned['TopTarget_HorID'] = df_new_cleaned[HorID_col]
        df_new_cleaned['TopHelper_DEPTH'] = df_new_cleaned[Pick_depth_col+'_x']
        df_new_cleaned['TopTarget_DEPTH'] = df_new_cleaned[Pick_depth_col]
        df_new_cleaned['TopHelper_HorID_Qual'] = df_new_cleaned[Quality_col+'_x']
        df_new_cleaned['TopTarget_Qual'] = df_new_cleaned[Quality_col]
        df_new_cleaned = df_new_cleaned[[SitID_col,lat,lng,UWI_col,'TopHelper_HorID','TopTarget_HorID','TopHelper_DEPTH','TopTarget_DEPTH','TopHelper_HorID_Qual','TopTarget_Qual']]
    return df_new_cleaned


def mergeCleanedAndUWIGeog_dfs(df_new_cleaned,UWIs_Geog):
    df_new_cleaned_plus_nn = pd.concat([df_new_cleaned, UWIs_Geog[['Neighbors_Obj']].copy()], axis=1)
    return df_new_cleaned_plus_nn


#### Neighbors_Obj must be 10th Col!!

def broadcastFuncForFindNearestNPickDepth(df_new_cleaned_plus_nn,pickColInt,newPickColName,UWI_col):
    """
    Takes in:
    Returns: 
    """
    df = df_new_cleaned_plus_nn
    #### For each row in dataframe,
    df[newPickColName] = np.nan
    print( df.iloc[0:1][newPickColName])
    for eachRow in range(len(df)):
        #print("len(df)",len(df))
        #### Find the nearest neighbor UWI
        #print(eachRow)
        UWI = df.iloc[eachRow,10][1][UWI_col]
        #print(type(UWI),"type to right of ",UWI)
        #### With the UWI from above, find the pickDepthName
        index_of_neigh_UWI = df.set_index(UWI_col).index.get_loc(UWI)
        #print("index_of_neigh_UWI= ",index_of_neigh_UWI)
        pick_depth = df.iloc[index_of_neigh_UWI,pickColInt]
        #print("pick_depth ",pick_depth)
        try:
            pick_depth = float(pick_depth)
        except:
            UWI = df.iloc[eachRow,10][2][UWI_col]
            index_of_neigh_UWI = df.set_index(UWI_col).index.get_loc(UWI)
            pick_depth = df.iloc[index_of_neigh_UWI,pickColInt]
            try:
                pick_depth = float(pick_depth)
            except:
                UWI = df.iloc[eachRow,10][3][UWI_col]
                index_of_neigh_UWI = df.set_index(UWI_col).index.get_loc(UWI)
                pick_depth = df.iloc[index_of_neigh_UWI,pickColInt]
                try:
                    pick_depth = float(pick_depth)
                except:
                    UWI = df.iloc[eachRow,10][4][UWI_col]
                    index_of_neigh_UWI = df.set_index(UWI_col).index.get_loc(UWI)
                    pick_depth = df.iloc[index_of_neigh_UWI,pickColInt]
                    try:
                        pick_depth = float(pick_depth)
                    except:
                        pick_depth = "no_pick"
            
        #### Write the pickDepthName to a new column
#         df[newPickColName][eachRow] = pick_depth
        eachRowP1 = eachRow+1
        df.iloc[eachRow:eachRowP1][newPickColName] = pick_depth
    return df

def convertStringToFloat(string):
    """
    Takes in:
    Returns: 
    """
    try:
        string = float(string)
    except:
        string = 0
    return string

def useThicknessOfNeighborsToEst(df_new2):
    df_new2['NN1_topTarget_DEPTH'] = df_new2['NN1_topTarget_DEPTH'].apply(convertStringToFloat)
    df_new2['NN1_TopHelper_DEPTH'] = df_new2['NN1_TopHelper_DEPTH'].apply(convertStringToFloat)
    df_new2['TopHelper_DEPTH'] = df_new2['TopHelper_DEPTH'].apply(convertStringToFloat)
    df_new2['TopTarget_DEPTH'] = df_new2['TopTarget_DEPTH'].apply(convertStringToFloat)
    df_new2['NN1_thickness'] = df_new2['NN1_TopHelper_DEPTH'] - df_new2['NN1_topTarget_DEPTH']
    # df_new2['trainOrTest'] = df_new2['trainOrTest']
    df_new2['topTarget_Depth_predBy_NN1thick'] =  df_new2['TopHelper_DEPTH'] - df_new2['NN1_thickness'] 
    return df_new2


def create_MM_Top_Depth_Real_v_predBy_NN1thick(df_new3):
    """
    Takes in:
    Returns: 
    """
    df_new3['MM_Top_Depth_Real_v_predBy_NN1thick'] =  df_new3['TopTarget_DEPTH'] - df_new3['topTarget_Depth_predBy_NN1thick'] 
    return df_new3

def onlyWellsInTestPortion(df,string_train_or_test):
    """
    Takes in:
    Returns: 
    """
    df_just_trainOrMaybeTest = df.loc[df['trainOrTest'] == string_train_or_test]
    print('len(df_just_trainOrMaybeTest)',len(df_just_trainOrMaybeTest))
    print("len(df_just_trainOrMaybeTest['UWI'].unique())",len(df_just_trainOrMaybeTest["UWI"].unique()))
    return df_just_trainOrMaybeTest

def fullWellsKNN(wells_df_from_split,input_data_inst,config):
    """
    Takes in:
    Returns: 
    """
    print("len(wells_df_from_split)",len(wells_df_from_split))
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
    print("len(df_new )",len(df_new ))
    ################ Let's limit the GIS and pick information dataframe to only the wells we're going to use and ###################
    ################ exclude any we're not going to use for not having the needed tops and curves. ###################
    ################ We'll have to change the format of the UWU col slightly to do this ###################
    wellsLoaded_list = createListOfWellNamesLoadedSplit(wells_df_from_split,config)
    new_wells_loaded_list_inUWIstyle = findListOfConvertedUWInamesForWellsLoaded(wells_df_from_split,config.UWI,input_data_inst.well_format)
    print("new_wells_loaded_list_inUWIstyle[5:8]",new_wells_loaded_list_inUWIstyle[5:8])
    print("len(new_wells_loaded_list_inUWIstyle )",len(new_wells_loaded_list_inUWIstyle))
    ################ This next step will reduce the total number of wells to just the ones that have at least the tops and curves we need ################ 
    df_reduced = reduced_df_from_split_plus_more(df_new,new_wells_loaded_list_inUWIstyle,config.UWI)
    print("len(df_reduced)",len(df_reduced))
    ################ We'll now find nearest N neighbors using a kdtree approach ################ 
    tree, dist, ind = kdtree(df_reduced, input_data_inst.gis_lat_col, input_data_inst.gis_long_col, config.kdtree_leaf, config.kdtree_k)
    UWIs_Geog = makeKNearNeighObj(df_reduced,config.UWI,input_data_inst.gis_lat_col, input_data_inst.gis_long_col,dist,ind,config.kdtree_k)
    print("UWIs_Geog.head()",UWIs_Geog.head())
    ################# Now to clean the dataframe, rename columns, and merge with the new dataframe that has the neighbors! ##################
    df_new_cleaned = cleanRenameDF(df_reduced,target, target_base,config,input_data_inst)
    df_new_cleaned_plus_nn = mergeCleanedAndUWIGeog_dfs(df_new_cleaned,UWIs_Geog)
    print("len(df_new_cleaned_plus_nn)",len(df_new_cleaned_plus_nn))
    print("This is how to access the data on nearest neigbhors in the 'Neighbors_Obj' column - df_new_cleaned_plus_nn.loc[1:1,'Neighbors_Obj'][1][1] =",df_new_cleaned_plus_nn.loc[1:1,'Neighbors_Obj'][1][1])
    print("an example of neighbors is : df_new_cleaned_plus_nn.loc[1:2,'Neighbors_Obj'][2] which is = ",df_new_cleaned_plus_nn.loc[1:2,'Neighbors_Obj'][2])
    ################# 6 and 7 in the functions below are the 6th and 7th columns... should replace with something more obvious!!!!! ##################
    df_new_cleaned_plus_nn_temp = broadcastFuncForFindNearestNPickDepth(df_new_cleaned_plus_nn, 7, config.NN1_topTarget_DEPTH, config.UWI)
    df_new2 = broadcastFuncForFindNearestNPickDepth(df_new_cleaned_plus_nn_temp, 6, config.NN1_TopHelper_DEPTH, config.UWI)
    df_new3 = useThicknessOfNeighborsToEst(df_new2)
    print("len(df_new3)",len(df_new3))
    print("printing first row of df_new2 in wellKNN_runner.py",df_new3[0:1])
    df_new4 = create_MM_Top_Depth_Real_v_predBy_NN1thick(df_new3)
    print("len(df_new4)",len(df_new4))
    return df_new4



def getTestRowsOnlyPicksDF(df,wellsLoaded_df_fromh5_newUWI,config,whichTrainOrTest_str,well_file_ending):
    #### funtion that takes in curves df and gets lists of test only wells
    wells_test_only = wellsLoaded_df_fromh5_newUWI.loc[wellsLoaded_df_fromh5_newUWI[config.trainOrTest] == whichTrainOrTest_str]
    #print(wells_test_only.head())
    #print(wells_test_only['UWI'].unique())
    UWI_test = list(wells_test_only[config.UWI].unique())
    print("len(UWI_test)",len(UWI_test))
    UWI_test_new = []
    for well_name in list(UWI_test):
        UWI_test_new.append(changeLASfileToBeUWIstr(well_name,well_file_ending))
    print("UWI_test[0]",UWI_test_new[0])
    print("df[config.UWI][0]",df[config.UWI][0])
    #### function that takes in list of test only wells and picks df and returns only well from picks dataframe that match
    df_new = df[df[config.UWI].isin(UWI_test_new)]
    #### returns dataframe
    print("len(df_new)",len(df_new))
    return df_new



