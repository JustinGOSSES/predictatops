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
import pickle
import math
import dask
import dask.dataframe as dd
from dask.distributed import Client
# import pdvega
# import vega
import random
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import mean_squared_error
import os

###### IMPORT FROM PREVIOUS SCRIPT IN WORKFLOW TWO HELPER FUNCTIONS ######
from features import getMainDFsavedInStep, load_prev_results_at_path


######################  Purpose is to duplicate some of the rows near the pick so they are more common  ######################
######################  and take out some of the rows farther away in training dataset, so they are less common  ######################
######################

#####################   Originally based on Mannville notebook PreML_ClassRebalence_FeatureSelection_Prep_20181003_vF #####################  


# What dataframes to get out of this notebook:

#     Dataframes of:
#         Dataframe with everything
#         Dataframe with only training data (with class rebalancing & no index values that might leak)
#         Dataframe with only training labels (with class rebalancing & no index values that might leak)
#         Dataframe with only test data (with no class rebalancing & no index values that might leak)
#         Dataframe with only test labels (with no class rebalancing & no index values that might leak)
#         Dataframes for each of the 4 above but also with indexes like UWI and DEPT which were kept off
#     Order of creation:
#         Split into train/test dataframes
#         Rebalance only training dataset
#         Split into test data, test label, train data, train label
#         Save versions with ONLY index colummns (UWI & Depth)
#         Take off (UWI & Depth & Others)
#         Save versions with only relevent information
#         Do ML


##### Contents

######     Read In a HDF5 from the previous notebook that creates the features
######     Add column for train or test based on a split %, like 80%/20%, split based on well UWI
######     Rebalance the classes by throwing out some of the rows away from the pick and duplicating some rows at or near the known pick.
######     Identify which columns to use as training features
######     Identify which columns to use as labels
######     Split single dataframe into 4 for train-features,train-labels,test-features,test-labels
######     Machine learning using standard XGBoost classifier and not yet Dask
######     Evaluate the initial results
######     Turning row-by-row classification prediction into single well pick depth prediction

# print(welly.__version__)
# print(dask.__version__)
# print(pd.__version__)
#######  0.3.5
#######  0.18.2
#######  0.23.3


###################### LOAD PREVIOUS CREATED DATASET WITH FEATURES ########################################################


def get_features_df_results(output_data_inst):
    """
    Takes in 
    Returns
    """
    #### get parts of the path to the resulting dataframe from wellsKN from the output_data_inst variable
    path_to_prev_results = output_data_inst.base_path_for_all_results
    path_to_directory = output_data_inst.path_features
    file_name = output_data_inst.features_results_wells_df
    ending = output_data_inst.default_results_file_format
    ##### combine all those variables into a single 

    full_path_to_features_results = getMainDFsavedInStep(path_to_prev_results,path_to_directory,file_name,ending)
    ##### load dataframe from full path
    wells_df_from_features_results  = load_prev_results_at_path(full_path_to_features_results)
    return wells_df_from_features_results



###################### Split into training and test dataframes ########################################################

def takeInDFandSplitIntoTrainTestDF(df,config):
    """
    Splits single input df into two dataframes, one test and one train, based on column values already assigned for train & test.
    Assumes that column in config.trainOrTest has values of only "train" or "test" and nothing else and no capitalization. A test should be written for this!
    """
    trainOrTest_col = config.trainOrTest
    df_all_Col_preSplit = df
    df_all_Col_train_noRebalance = df_all_Col_preSplit.loc[df_all_Col_preSplit[trainOrTest_col ] == 'train']
    df_all_Col_test = df_all_Col_preSplit.loc[df_all_Col_preSplit[trainOrTest_col ] == 'test']
    return df_all_Col_train_noRebalance, df_all_Col_test





##### Rebalance class, aka label, populations to deal with lopsided class populations
##### Because we have a lot more rows far away from the pick than exactly at the pick or close to the pick, we run the risk of being class heavy in some areas. This can result in not enough ability to identify the sparsely populate classes, like right at the pick.
##### We'll attemp to deal with this problem by throwing out some of the rows far away from the pick and duplicating some of the rows right at or near the pick.
##### THIS SHOULD ONLY BE DONE TO THE TRAINING DATA NOT THE TEST DATA OR THAT IS CHEATING!
###################### Rebalance class, aka label, populations to deal with lopsided class populations ########################################################
############################# THIS SHOULD ONLY BE DONE TO THE TRAINING DATA NOT THE TEST DATA OR THAT IS CHEATING! ##########3

def countRowsByClassOfNearPickOrNot(df,arrayOfClass,divisionInt,classToShrink):
    """
    Takes as input a dataframe, array of classes, an integer to divide by, and  a column, and a class within the column to shrink.
    Returns the dataframe minus the rows that match the ClassToShrink in the Col and prints details about the number of rows of the various classes.
    """
    for eachClass in arrayOfClass:
        print("length of rows with "+str(eachClass)+" in class_DistFrPick_TopTarget:",len(df[df['class_DistFrPick_TopTarget'] == eachClass]))
    df_NearPickZeroSmall = df.loc[(df.index%10 != 3) & (df['class_DistFrPick_TopTarget'] == classToShrink)]
    print("length of rows with 0 in class_DistFrPick_TopTarget and %"+str(divisionInt)+" == 0 is:",len(df_NearPickZeroSmall))
    print("% reduction in classs 0 is:", math.floor(len(df_NearPickZeroSmall) / len(df['class_DistFrPick_TopTarget'] == classToShrink) * 100),"%")
    total_after_reduction_in_bigger_class = len(df[df['class_DistFrPick_TopTarget'] == classToShrink]) -len(df_NearPickZeroSmall)
    print("if taken out using this remainder, the total number of 0 class will be: ",total_after_reduction_in_bigger_class)
#     print("ratio between that class away from pick and classes near pick is :":)
    return df_NearPickZeroSmall

##### example of how to run countRowsByClassOfNearPickOrNot() function.
##### class_array_NearPick = [100,95,70,60,0]
##### test_df_return = countRowsByClassOfNearPickOrNot(df_test_5,class_array_NearPick,2,0)

def getListOfKeysForZonesObj(config):
    """
    Takes in the configuration object 
    Returns the keys of the zonesAroundTops object in configuration class
    """
    class_array_NearPick = list(config.zonesAroundTops.keys())
    return class_array_NearPick


def dropsRowsWithMatchClassAndDeptRemainderIsZero(df,Col,RemainderInt,classToShrink):
    """
    Takes as input a dataframe, a column, a remainder integer, and a class within the column.
    Returns the dataframe minus the rows that match the ClassToShrink in the Col and have a depth from the DEPT col with a remainder of zero.
    """
    print("original lenght of dataframe = ",len(df))
    df_new = df.drop(df[(df[Col] == classToShrink) & (df.index%10 != 0)].index)
    print("length of new dataframe after dropping rows = ",len(df_new))
    print("number of rows dropped = ",len(df)-len(df_new))
    print("length of 0 class is :",len(df_new[df_new[Col] == classToShrink]))
    return df_new


# df_all_Col_preSplit_wTrainTest_ClassBalanced = dropsRowsWithMatchClassAndDeptRemainderIsZero(df_all_Col_train_noRebalance,'class_DistFrPick_TopTarget',7,0)

# df_all_Col_preSplit_wTrainTest_ClassBalanced.info()


def addsRowsToBalanceClasses(df,rangeFor100,rangeFor95):
    """
    Input is a dataframe, range for class 100, and range for class 95
    Copies the rows with labels that don't occur very much so they are a larger part of dataframe
    returns the new dataframe with additional copies of rows added on
    """
    df_class100 = df[df['class_DistFrPick_TopTarget'] == 100]
    df_class95 = df[df['class_DistFrPick_TopTarget'] == 95]
    for each1 in range(rangeFor100):
        #print(each1)
        df = df.append(df_class100, ignore_index=True)
    for each2 in range(rangeFor95):
        #print(each2)
        df = df.append(df_class95, ignore_index=True)
    return df

#### EXAMPLE OF
#### #### now we duplicate some rows for the class that wasn't well populated.
#### df_all_Col_preSplit_wTrainTest_ClassBalanced2 = addsRowsToBalanceClasses(df_all_Col_preSplit_wTrainTest_ClassBalanced,50,10)


def findNumberOfEachClass(df,col):
    return df[col].value_counts()

#### findNumberOfEachClass(df_all_Col_preSplit_wTrainTest_ClassBalanced2,'class_DistFrPick_TopTarget')

##### len(df_all_Col_preSplit_wTrainTest_ClassBalanced2)

#####df_all_Col_preSplit_wTrainTest_ClassBalanced2.info()

##### df_all_Col_preSplit_wTrainTest_ClassBalanced = df_all_Col_preSplit_wTrainTest_ClassBalanced2

##### col_list = df_all_Col_preSplit_wTrainTest_ClassBalanced.columns
##### print(col_list)

##### col_list = list(col_list)
##### col_list

########### Manually copy the list above and take out some that are labels or aren't things you want to use as training #######
##################### At some point come back and see if I can instead use a standard list of things to not include and make the list of columns to use as features more automatically???  ############

####### Two lists of columns to not use as training features, Columns taken out as they aren't present often enough in the well dataset

######### Columns taken out as they either contain information probably captures in other columns, are related to labels too closely, or other reasons.
############## BUT LEAVE IN THE 'class_DistFrPick_TopTarget' column for now as thats a label we'll use in label df!!!!

#### THESE ARE DEFINED IN CONFIG CLASS!  ########
#### columns_to_not_trainOn_andNotCurves = config.columns_to_not_trainOn_andNotCurves
#### columns_to_not_trainOn_andAreCurves = config.columns_to_not_trainOn_andAreCurves

############## Next few lines to combine the two lists above and take those columns out of dataframe

def takeOutColNotNeededInTrainingDF(df,list_allCol,colToTakeOutCurves,colToTakeOutOther):
    print("number of columns in dataframe coming into function",len(df.columns))
    train_feats_minusLowCount = [x for x in list_allCol if x not in colToTakeOutCurves]
    train_feats_minusLowCount = [x for x in train_feats_minusLowCount if x not in colToTakeOutOther]
    df_train_featWithHighCount = df[train_feats_minusLowCount]
    print("number of columns in dataframe leaving function",len(df_train_featWithHighCount.columns))
    return df_train_featWithHighCount


# df_train_featWithHighCount = takeOutColNotNeededInTrainingDF(df_all_Col_preSplit_wTrainTest_ClassBalanced,col_list,training_feats_w_lowCount,takeOutColumnsNotCurvesList)


# list(df_train_featWithHighCount.columns)


##############  Number of columns for training
# len(df_train_featWithHighCount.columns)

# df_train_featWithHighCount.describe()

# used_features = list(df_train_featWithHighCount.columns)
# used_features 

#####################   Now let's take out those same columns in the test only dataframe
#df_test_featWithHighCount = takeOutColNotNeededInTrainingDF(df_all_Col_test,col_list,training_feats_w_lowCount,takeOutColumnsNotCurvesList)

################ Now let's combine the rebalanced train df with the unrebalanced test df to make a df we will then split into 4 pieces: train-data, train-labels, test-data,test-lables
# df_testPlusRebalTrain_featWithHighCount = pd.concat([df_train_featWithHighCount,df_test_featWithHighCount])
# len(df_testPlusRebalTrain_featWithHighCount.columns)

def combineRebalancedTrainDFWithUnrebalancedTestDF(df_train_featWithHighCount,df_test_featWithHighCount):
    """
    Now let's combine the rebalanced train df with the unrebalanced test df to make a df we will then split into 4 pieces: train-data, train-labels, test-data,test-lables
    """ 
    df_testPlusRebalTrain_featWithHighCount = pd.concat([df_train_featWithHighCount,df_test_featWithHighCount])
    return df_testPlusRebalTrain_featWithHighCount



# Identify which columns to use as labels
# The column 'cat_isTopMcMrNearby_known' is what we'll use as labels.

#     100 = exactly the Top McMurray Pick
#     95 if the distance between that depth and the Top McMurray Pick is -0.5 < x and x <0.5
#     60 if the distance between that depth and the Top McMurray Pick is -5 < x and x < 5
#     0 = not near the Top McMurray Pick

# The function used to make these classes or lables as column was: df_all_wells_wKNN_DEPTHtoDEPT['cat_isTopMcMrNearby_known']=df_all_wells_wKNN_DEPTHtoDEPT['diff_TMcM_Pick_v_DEPT'].apply(lambda x: 100 if x==0 else ( 95 if (-0.5 < x and x <0.5) else 60 if (-5 < x and x <5) else 0))

# df_testPlusRebalTrain_featWithHighCount['class_DistFrPick_TopTarget'].unique()
# labels = df_testPlusRebalTrain_featWithHighCount[['class_DistFrPick_TopTarget','UWI','trainOrTest','TopTarget_DEPTH']]

# labels.head()

# labels.tail()

# len(labels)

############### e lengths of training dataframes and labels dataframes should be the same. We'll take out UWI and trainOrTest further down.


##########################################################################################
# Now separate into 4 dataframes =
# train_labels
# train_feat
# test_labels
# test_feat

# Then take off UWI and TrainTest col
##########################################################################################
# Create label dataframes



def makeDFofJustLabels(df,config):
    """
    write here
    """
    columns_to_use_as_labels = config.columns_to_use_as_labels  ##### ['class_DistFrPick_TopTarget','UWI','trainOrTest','TopTarget_DEPTH']
    labels_df = df[columns_to_use_as_labels]
    return labels_df



##############     Now separate into 4 dataframes =    ###########
# train_labels
# train_feat
# test_labels
# test_feat

# Then take off UWI and TrainTest col

def make4separateDF(labels,df_testPlusRebalTrain_featWithHighCount,config):
    """
    Things
    """
    trainOrTest_str = config.trainOrTest
    ###### Create label dataframes
    #### split based on train in trainOrTest col
    labels_train = labels[labels['trainOrTest'] == 'train' ]
    #### Keep only the 'cat_isTopMcMrNearby_known' column, so now it is just a series of labels
    labels_train = labels_train['class_DistFrPick_TopTarget']
    #### split based on test in trainOrTest col
    labels_test = labels[labels['trainOrTest'] == 'test' ]
    #### Keep only the 'cat_isTopMcMrNearby_known' column, so now it is just a series of labels
    labels_test = labels_test['class_DistFrPick_TopTarget']
    #### rename 
    df_train_featWithHighCount = df_testPlusRebalTrain_featWithHighCount
    ###### Create training dataframes
    print("columns that are being treated as labels and dropped/added accordinating are:",config.columns_to_use_as_labels," from configuration class instance attribute 'columns_to_use_as_labels'")
    #### split based on train in trainOrTest col and drop UWI and TrainOrTest columns
    df_train_featWithHighCount_train = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount[trainOrTest_str] == 'train' ].drop(columns=config.columns_to_use_as_labels)
    #### split based on test in trainOrTest col and drop UWI and TrainOrTest columns
    df_train_featWithHighCount_test = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount[trainOrTest_str] == 'test' ].drop(columns=config.columns_to_use_as_labels)
    ###### Create index dataframes for :
    ###### reattaching'UWI', 'trainOrTest','class_DistFrPick_TopTarget','TopTarget_DEPTH'
    df_train_featWithHighCount_train_indexOnly = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount[trainOrTest_str] == 'train'][config.columns_to_use_as_labels]
    df_train_featWithHighCount_test_indexOnly = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount[trainOrTest_str] == 'test' ][config.columns_to_use_as_labels]
    #print("df_train_featWithHighCount_train_indexOnly.head()",df_train_featWithHighCount_train_indexOnly.head())
    #### Rename to avoid overwriting & keep with previous work
    train_X = df_train_featWithHighCount_train
    train_y = labels_train
    test_X = df_train_featWithHighCount_test
    test_y = labels_test
    train_index = df_train_featWithHighCount_train_indexOnly
    test_index = df_train_featWithHighCount_test_indexOnly 
    #### Inspect to make sure column headers and lengths make sense
    #### MAKE A TEST HERE, LENGTH SHOULD BE THE SAME BEWEEN 1 & 2 and 3 & 4 ! ####
    ## print(len(train_X))
    ## train_X.head()
    ## print(len(train_y))
    ## train_y.head()
    ## print(len(test_X))
    ## test_X.head()
    ## print(len(test_y))
    ## test_y.head()
    if len(train_X) != len(train_y):
        print("THERE MAY BE A ERROR WHILE REBALANCEING train_X and train_y ARE NOT SAME LENGTH")
    else:
        pass
    if len(test_X) != len(test_y):
        print("THERE MAY BE A ERROR WHILE REBALANCEING test_X and test_y ARE NOT SAME LENGTH")
    else:
        pass
    return df_testPlusRebalTrain_featWithHighCount, train_X, train_y, test_X, test_y, train_index, test_index

########################################
# Save the dataframes as a dict
#     train_X
#     train_y
#     test_X
#     test_y
#     & full

def saveRebalanceResultsAsHDF(df_testPlusRebalTrain_featWithHighCount, train_X, train_y, test_X, test_y, train_index, test_index, output_data_inst):
    """
    Takes in 
    Saves 
    Returns 
    """
    ###### Establish file path to save 
    load_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_balance
    load_results_full_file_path = load_dir+"/"+output_data_inst.balance_results_wells_df+output_data_inst.default_results_file_format
    #########################  Write each pandas dataframes to single HDF5 using separate keys to retrieve later
    df_testPlusRebalTrain_featWithHighCount.to_hdf(load_results_full_file_path, key='preSplitpreBal', mode='w')
    train_X.to_hdf(load_results_full_file_path, key='train_X')
    train_y.to_hdf(load_results_full_file_path, key='train_y')
    test_X.to_hdf(load_results_full_file_path, key='test_X')
    test_y.to_hdf(load_results_full_file_path, key='test_y')
    train_index.to_hdf(load_results_full_file_path, key='train_index')
    test_index.to_hdf(load_results_full_file_path, key='test_index')
    print("finished saving the results of the rebalancing script in the location set in the output class instance. = ",load_results_full_file_path)






###################### LOAD PREVIOUS CREATED DATASET WITH FEATURES ########################################################