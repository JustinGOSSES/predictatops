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
#from dask.distributed import Client
#from distributed import Client
from distributed.client import *

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



################ Load dataframe of tops data from wellsKNN script ###################

def getMainDFsavedInStep(path_to_results,path_to_directory,file_name,ending):
    """
    Takes in 
    Returns
    """
    dir_path = path_to_results + "/" + path_to_directory
    full_path_to_results_file = dir_path+"/"+file_name+ending
    return full_path_to_results_file

def load_prev_results_at_path(full_path_to_results_file,key='df'):
    """
    Takes in 
    Returns
    """
    wells_df_from_wellsKNN  = pd.read_hdf(full_path_to_results_file,key=key)
    return wells_df_from_wellsKNN

def get_wellsKNN_results(output_data_inst):
    """
    Takes in 
    Returns
    """
    #### get parts of the path to the resulting dataframe from wellsKN from the output_data_inst variable
    path_to_prev_results = output_data_inst.base_path_for_all_results
    path_to_directory = output_data_inst.path_wellsKNN
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
    #### check if UWI column exists in each dataframe, if not, find SitID and create UWI column from SiteID
    
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
    df_all_wells_wKNN[columns_to_turn_to_floats] = df_all_wells_wKNN[columns_to_turn_to_floats].astype(float)
    return df_all_wells_wKNN

def takeLASOffUWI(df,config):
    """
    Change UWI string .LAS to just UWI string
    """
    df[config.UWI] = df[config.UWI].str.replace(".LAS","")
    return df

def convertSiteIDListToUWIList(input_data_inst,df_with_sitID):
        """doc string goes here"""
        if input_data_inst.wells_df is not None:
            wells = input_data_inst.load_wells_file()
        else:
            wells = input_data_inst.input.wells_df
        # if self.wells_with_all_given_tops is not None:
        #     wells_with_all_given_tops = self.findWellsWithAllTopsGive()
        # else:
        #     wells_with_all_given_tops = self.wells_with_all_given_tops
        wells = wells[['SitID','UWI']]
        #wells["UWInew"] = wells["UWI"].str.replace("/","-")+".LAS"
        wells["UWInew"] = wells["UWI"].str.replace("/","-")+".LAS"
        wells = wells[['SitID','UWInew']]
        wells_dict = wells.set_index('SitID').T.to_dict('r')[0]
        print("wells_dict = ",wells_dict)
        #df_with_sitID['UWI'] = df_with_sitID['SitID']
        #df_with_sitID.replace({'UWI': wells_dict},inplace=True)
        df_with_sitID['UWI'] = df_with_sitID['SitID'].map(wells_dict)
        #df_with_sitID['UWI'] = df_with_sitID['UWI'][1]
        #df_with_sitID['UWI'] = wells_dict[df_with_sitID['SitID']][1]
        print("df_with_sitID[0:2]",df_with_sitID.UWI)
        return df_with_sitID

################################################## #####################################
########## ALL THE NEXT FEW FUNCTIONS BELOW CREATES FEATURES AS COL IN  ################
########## DATAFRAME HAVING TO DO WITH NEAREST NEIGHBOR AND DEPTH IN WELL ##############
########## AND RELATIVE TO KNOWN PICKS #################################################

def createDepthRelToKnownTopInSameWell(df):
    """
    Create columns for how close a row is (based on depth) from the official pick for that well.
    We'll be doing this for Top and Base McMurray in the example.
    Returns the input dataframe with additional column(s)
    #### IT SHOULD BE NOTED THAT THE 'correct' PICK DEPTHS IN MANY CASES DO NOT PERFECTLY MATCH THE DEPTHS AVAILABLE IN THE LOGS.
    #### In other words, the pick might be 105 but there is no row with 105.00 depth, only a 104.98 and a 105.02!
    #### This matters for what you count as a correct label!
    """
    df_all_wells_wKNN_DEPTHtoDEPT = df
    #### for top McMurray
    df_all_wells_wKNN_DEPTHtoDEPT['diff_TopTarget_DEPTH_v_rowDEPT'] = df_all_wells_wKNN_DEPTHtoDEPT['TopTarget_DEPTH'] - df_all_wells_wKNN_DEPTHtoDEPT['DEPT']
    #### for base McMurray or Top Paleozoic
    df_all_wells_wKNN_DEPTHtoDEPT['diff_TopHelper_DEPTH_v_rowDEPT'] = df_all_wells_wKNN_DEPTHtoDEPT['TopHelper_DEPTH'] - df_all_wells_wKNN_DEPTHtoDEPT['DEPT']
    return df_all_wells_wKNN_DEPTHtoDEPT

def createFeat_withinZoneOfKnownPick(df,config):
    """
    Input is 3 parts. 
    First part is: dataframe with tops & curve data for feature creation after wellsKNN step.
    Second part is: A dict consisting of keys that are the labels for each zone values which are a list with two items, the min and max for that zone.
    For example: {100:[0],95:[-0.5,0.5],60:[-5.0.5],70:[0.5,<5],0:[]}
    NOTE: The code in createFeat_withinZoneOfKnownPick(df,config) function in features.py current ASSUMES only 5 zone labels

    #### Create a column that has a number that symbolizes whether a row is close or not to the 'real' pick
    #### We'll do this first for Top McMurray and then top Paleozoic, which is basically base McMurray
    """
    df_all_wells_wKNN_DEPTHtoDEPT = df
    zonesAroundTops = config.zonesAroundTops
    zones = list(zonesAroundTops.keys())
    #### CHANGE => diff_TMcM_Pick_v_DEPT
    df_all_wells_wKNN_DEPTHtoDEPT['class_DistFrPick_TopTarget']=df_all_wells_wKNN_DEPTHtoDEPT['diff_TopTarget_DEPTH_v_rowDEPT'].apply(lambda x: zones[0] if x==zonesAroundTops[zones[0]][0] else ( zones[1] if (zonesAroundTops[zones[1]][0] < x and x <= zonesAroundTops[zones[1]][1]) else zones[2] if (zonesAroundTops[zones[2]][0] < x and x <= zonesAroundTops[zones[2]][1]) else zones[3] if (zonesAroundTops[zones[3]][0] < x and x <= zonesAroundTops[zones[3]][1]) else zones[4]))
    #### Top paleozoic version
    df_all_wells_wKNN_DEPTHtoDEPT['class_DistFrPick_TopHelper']=df_all_wells_wKNN_DEPTHtoDEPT['diff_TopTarget_DEPTH_v_rowDEPT'].apply(lambda x: zones[0] if x==zonesAroundTops[zones[0]][0] else ( zones[1] if (zonesAroundTops[zones[1]][0] < x and x <= zonesAroundTops[zones[1]][1]) else zones[2] if (zonesAroundTops[zones[2]][0] < x and x <= zonesAroundTops[zones[2]][1]) else zones[3] if (zonesAroundTops[zones[3]][0] < x and x <= zonesAroundTops[zones[3]][1]) else zones[4]))

    # df_all_wells_wKNN_DEPTHtoDEPT['class_DistFrPick_TopHelper']=df_all_wells_wKNN_DEPTHtoDEPT['diff_TopHelper_DEPTH_v_rowDEPT'].apply(lambda x: 100 if x==0 else ( 95 if (-0.5 < x and x <0.5) else 60 if (-5 < x and x <-0.5) else 70 if (0.5 < x and x <5) else 0))
    return df_all_wells_wKNN_DEPTHtoDEPT


def NN1_TopMcMDepth_Abs(df,config):
    """
    ### Takes MM_Top_Depth_predBy_NN1thick and subtracts depth at that point, returns *absolute* value
    """
    DEPT = config.DEPTH_col_in_featureCreation
    col_topTarget_Depth_predBy_NN1thick = config.col_topTarget_Depth_predBy_NN1thick
    df['DistFrom_NN1ThickPredTopDepth_toRowDept'] = abs(df[col_topTarget_Depth_predBy_NN1thick] - df[DEPT])
    return df

#### The difficult thing about creating features based on windows within a well when you have multiple wells stacked 
#### in a dataframe is that sometimes that window from one well goes into the next well.
#### To get around that, we're going create a column that says the distance from the top of the well and another 
#### column that says the distance form the bottom of the well. When a row's distance from top or bottom is greater 
#### than 1/2 the max window size, we'll just use proceed as normal. When the distance between that row's depth and
#### top or bottom is less than 1/2 the max window size, we'll 

def markingEdgeOfWells(df,config):
    """
    #### The difficult thing about creating features based on windows within a well when you have multiple wells stacked 
    #### in a dataframe is that sometimes that window from one well goes into the next well.
    #### To get around that, we're going create a column that says the distance from the top of the well and another 
    #### column that says the distance form the bottom of the well. When a row's distance from top or bottom is greater 
    #### than 1/2 the max window size, we'll just use proceed as normal. When the distance between that row's depth and
    #### top or bottom is less than 1/2 the max window size, we'll 
    """
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM = df

    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['NewWell'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['UWI'].shift(1) != df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['UWI']
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['LastBitWell'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['UWI'].shift(-1) != df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['UWI']

    TopOfWellRowsOnly = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM.loc[df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['NewWell'] == True]
    BottomOfWellRowsOnly = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM.loc[df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['LastBitWell'] == True]

    #rename depth to top and bottom depths , delete all other columns
    TopOfWellRowsOnly = TopOfWellRowsOnly[['UWI','DEPT']]
    TopOfWellRowsOnly['TopWellDept'] = TopOfWellRowsOnly['DEPT']
    TopOfWellRowsOnly.drop(['DEPT'],axis=1, inplace=True)
    #### same thing for bottom
    BottomOfWellRowsOnly = BottomOfWellRowsOnly[['UWI','DEPT']]
    BottomOfWellRowsOnly['BotWellDept'] = BottomOfWellRowsOnly['DEPT']
    BottomOfWellRowsOnly.drop(['DEPT'],axis=1, inplace=True)
    #### merge these two small dataframes
    TopAndBottomOfWellRowsOnly = pd.merge(TopOfWellRowsOnly, BottomOfWellRowsOnly, on='UWI')
    #### merge with larger dataframe
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM = pd.merge(df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM, TopAndBottomOfWellRowsOnly, on='UWI')
    
    ####
    #### Create a col for distance from row to top of well
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromTopWell'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['DEPT'] - df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['TopWellDept']

    #### Create a col for distance from row to bottom of well
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromBotWell'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['BotWellDept'] - df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['DEPT']

    #### Create col for well total thickness measured
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['WellThickness'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['BotWellDept'] - df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['TopWellDept']

    ####
    ####This adds a column that says whether a row is closer to the bottm or the top of the well
    ####This is useful for doing creation of features of rolling windows where you want to avoid going into another well stacked above.¶
    #### This adds a column that says whether a row is closer to the bottm or the top of the well
    #### This is useful for doing creation of features of rolling windows where you want to avoid going into another well stacked above.
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['closerToBotOrTop'] = np.where(df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromTopWell']<=df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromBotWell'], 'FromTopWell', 'FromBotWell')
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['closTopBotDist'] = np.where(df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromTopWell']<=df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromBotWell'], df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromTopWell'], df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['FromBotWell'])
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['rowsToEdge'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['closTopBotDist']/0.25
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['rowsToEdge'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['rowsToEdge'].astype(int)

    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['diff_DEPT_vs_NN1_topTarget_DEPTH'] = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['DEPT'] - df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM['NN1_topTarget_DEPTH']
    return df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM 


################################################## #####################################
########## ALL THE NEXT FEW FUNCTIONS BELOW CREATES FEATURES AS COL IN  ################
########## DATAFRAME HAVING TO DO WITH ANALYZING CURVES ACROSS WINDOWS #################
########## RELATIVE TO EACH DEPTH IN EACH WELL #########################################

def nLargest(array,nValues):
    """
    writes things here
    """
    answer = np.mean(array[np.argsort(array)[-nValues:]])  
    return answer

def thoughts_seperateRollingAndConditionalIntoTwoDaskProcesses(dd,curves,windows):
    """
    for loop for each combination of parameter for rolling functions
    curves = ['GR','ILD']
    windows = [5,7,11,21]
    directions = ["around","below","above"]
        #         Not sure the best way to do the 'below' centered rolling in dask as the sort_index is expensive in dask so might be slow!
        #       Skipping this for now will come back when not tired. Maybe use shift?
    For each column created, check window size vs. allowable window size column, if too small, use single row value from original column
    """
    comboArg_B = [curves,windows]
    all_comboArgs_B = list(itertools.product(*comboArg_B))
    for eachArgList in all_comboArgs_B:
        col = eachArgList[0]
        windowSize = eachArgList[1]
        #centered = eachArgList[2]
        featureName = col+"_min_"+str(windowSize)+"winSize_"
        half_window = int(windowSize/2)
        #         quarter_window = int(windowSize/4)

        
        ### goes through distance to edge and when less than windowSize writes "too close" otherwise returns NaN
        ### fills in Nan with calculated feature column
        ### replaces "too close" with NaN
        ### replaces NaN with dd[col]
        ### overrights original column
        
        #### MIN
        dd[featureName+'dir'+'Around'+'Min'] = dd[col].rolling(windowSize,center=True).min()
        dd[featureName+'dir'+'Around'+'Min'] = dd[featureName+'dir'+'Around'+'Min'].where(cond=dd['closTopBotDist'] > half_window, other=dd[col])
        
        dd[featureName+'dir'+'Above'+'Min'] = dd[col].rolling(windowSize,center=False).min()
        dd[featureName+'dir'+'Above'+'Min'] = dd[featureName+'dir'+'Above'+'Min'].where(cond=dd['closTopBotDist'] > windowSize, other=dd[col])
        print("finished min in function thoughts_seperateRollingAndConditionalIntoTwoDaskProcesses")
        ### MAX
        dd[featureName+'dir'+'Around'+'Max'] = dd[col].rolling(windowSize,center=True).max()
        dd[featureName+'dir'+'Around'+'Max'] = dd[featureName+'dir'+'Around'+'Max'].where(cond=dd['closTopBotDist'] > half_window, other=dd[col])
        
        dd[featureName+'dir'+'Above'+'Max'] = dd[col].rolling(windowSize,center=False).max()
        dd[featureName+'dir'+'Above'+'Max'] = dd[featureName+'dir'+'Above'+'Max'].where(cond=dd['closTopBotDist'] > windowSize, other=dd[col])
        #### Mean
        dd[featureName+'dir'+'Around'+'Mean'] = dd[col].rolling(windowSize,center=True).mean()
        dd[featureName+'dir'+'Around'+'Mean'] = dd[featureName+'dir'+'Around'+'Mean'].where(cond=dd['closTopBotDist'] > half_window, other=dd[col])
        
        dd[featureName+'dir'+'Above'+'Mean'] = dd[col].rolling(windowSize,center=False).mean()
        dd[featureName+'dir'+'Above'+'Mean'] = dd[featureName+'dir'+'Above'+'Mean'].where(cond=dd['closTopBotDist'] > windowSize, other=dd[col])
        print("finished mean in function thoughts_seperateRollingAndConditionalIntoTwoDaskProcesses")
        ## nLargest
        nValues = 5
        dd[featureName+'dir'+'Above'+'nLarge'] = dd[col].rolling(windowSize,center=False).apply( lambda x: nLargest(x,nValues),raw=True)  
        dd[featureName+'dir'+'Above'+'nLarge'] = dd[featureName+'dir'+'Above'+'nLarge'].where(cond=dd['closTopBotDist'] > windowSize, other=dd[col])
        
        dd[featureName+'dir'+'Around'+'nLarge'] = dd[col].rolling(windowSize,center=True).apply(lambda x: nLargest(x,nValues),raw=True) 
        dd[featureName+'dir'+'Around'+'nLarge'] = dd[featureName+'dir'+'Around'+'nLarge'].where(cond=dd['closTopBotDist'] > windowSize, other=dd[col])
    
    return dd


def createManyFeatFromCurvesOverWindows_withDask(df,config):
    """
    asdf
    """
    ###
    #### To run Dask computations with only a subset of the full dataframe is sometimes useful for debugging as seen in line below.
    #### df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop = df[0:20000] 
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop = df

    ###
    #client = Client()
    client = Client(processes=False)
    #client
    test_5 = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop.copy()
    print("copied test_5")
    test_5 = dd.from_pandas(test_5, npartitions=50)
    print("type(test_5)",type(test_5))
    #curves = ['GR','ILD','NPHI','DPHI']
    curves = config.must_have_curves_list
    #windows = [5,7,11,21]
    windows = config.curve_windows_for_rolling_features

    #### The function nLargest is used via apply, I should probably re-write this to use Dask's Nlargest API 
    #### but didn't here as the docs imply it might behave slightly differently.
    #### A quick look at the status dashboard in the Dask Client suggests the use of apply takes up maybe 1/4-1/2 
    #### of total compute time currently!
    
    ddf_test5 = thoughts_seperateRollingAndConditionalIntoTwoDaskProcesses(test_5,curves,windows)
    print("NOTE: currently in createManyFeatFromCurvesOverWindows(df,config) function & calculated graph for ddf_test5. This will take a while to compute() via Dask, so sit tight!")
    test5result = ddf_test5.compute()
    print("test5result.head()",test5result.head())
    print("type(test5result)",type(test5result))
    print("len(test5result.columns)",len(test5result.columns))
    return test5result

########### MIGHT HAVE ALREADY ADDED IN THIS , BUT CHECK #####
#test5result['diff_DEPT_vs_NN1_topTarget_DEPTH'] = test5result['DEPT'] - test5result['NN1_topTarget_DEPTH']


def createManyFeatFromCurvesOverWindows_withOutDask(df,config):
    """
    asdf
    """
    ###
    #### To run Dask computations with only a subset of the full dataframe is sometimes useful for debugging as seen in line below.
    #### df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop = df[0:20000] 
    df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop = df

    ###
    #client = Client()
    #client = Client(processes=False)
    #client
    #test_5 = df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop.copy()
    #print("copied test_5")
    #test_5 = dd.from_pandas(test_5, npartitions=50)
    #print("type(test_5)",type(test_5))
    #curves = ['GR','ILD','NPHI','DPHI']
    curves = config.must_have_curves_list
    #windows = [5,7,11,21]
    windows = config.curve_windows_for_rolling_features

    #### The function nLargest is used via apply, I should probably re-write this to use Dask's Nlargest API 
    #### but didn't here as the docs imply it might behave slightly differently.
    #### A quick look at the status dashboard in the Dask Client suggests the use of apply takes up maybe 1/4-1/2 
    #### of total compute time currently!
    print("started to run long function to create features in createManyFeatFromCurvesOverWindows_withOutDask(df,config), sit tight!")
    df_test5 = thoughts_seperateRollingAndConditionalIntoTwoDaskProcesses(df_all_wells_wKNN_DEPTHtoDEPT_KNN1PredTopMcM_NearTop,curves,windows)
    #print("NOTE: currently in createManyFeatFromCurvesOverWindows(df,config) function & calculated graph for ddf_test5. This will take a while to compute() via Dask, so sit tight!")
    #test5result = ddf_test5.compute()
    print("test5result.head()",df_test5.head())
    print("type(test5result)",type(df_test5))
    print("len(test5result.columns)",len(df_test5.columns))
    print("len(df_test5)",len(df_test5))
    return df_test5


