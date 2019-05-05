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


######################  Purpose is to duplicate some of the rows near the pick so they are more common  ######################
######################  and take out some of the rows farther away in training dataset, so they are less common  ######################
###################### This will REBALANCE the classes in the dataset ##################################################################

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






###################### Split into training and test dataframes ########################################################




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

class_array_NearPick = [100,95,70,60,0]
test_df_return = countRowsByClassOfNearPickOrNot(df_test_5,class_array_NearPick,2,0)

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


df_all_Col_preSplit_wTrainTest_ClassBalanced = dropsRowsWithMatchClassAndDeptRemainderIsZero(df_all_Col_train_noRebalance,'class_DistFrPick_TopTarget',7,0)

df_all_Col_preSplit_wTrainTest_ClassBalanced.info()


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

df_all_Col_preSplit_wTrainTest_ClassBalanced2 = addsRowsToBalanceClasses(df_all_Col_preSplit_wTrainTest_ClassBalanced,50,10)


def findNumberOfEachClass(df,col):
    return df[col].value_counts()

findNumberOfEachClass(df_all_Col_preSplit_wTrainTest_ClassBalanced2,'class_DistFrPick_TopTarget')

len(df_all_Col_preSplit_wTrainTest_ClassBalanced2)

df_all_Col_preSplit_wTrainTest_ClassBalanced2.info()

df_all_Col_preSplit_wTrainTest_ClassBalanced = df_all_Col_preSplit_wTrainTest_ClassBalanced2

col_list = df_all_Col_preSplit_wTrainTest_ClassBalanced.columns
print(col_list)

col_list = list(col_list)
col_list

########### Manually copy the list above and take out some that are labels or aren't things you want to use as training #######
##################### At some point come back and see if I can instead use a standard list of things to not include and make the list of columns to use as features more automatically???  ############

####### Two lists of columns to not use as training features, Columns taken out as they aren't present often enough in the well dataset

training_feats_w_lowCount = ['RHOB','SP','CALI','COND','DELT','DENS','DPHI:1','DPHI:2','DT','GR:1','GR:2','IL','ILD:1','ILD:2','ILM','LITH','LLD','LLS','PHID','PHIN','RESD','RT','SFL','SFLU','SN','SNP','Sp']


######### Columns taken out as they either contain information probably captures in other columns, are related to labels too closely, or other reasons.
############## BUT LEAVE IN THE 'class_DistFrPick_TopTarget' column for now as thats a label we'll use in label df!!!!

takeOutColumnsNotCurvesList = [
    'FromBotWell',
    'FromTopWel'
    'rowsToEdge',
     'lat',
     'lng',  
 'SitID',
 'TopHelper_HorID',
 'TopTarget_HorID',
 'TopHelper_DEPTH',
 'diff_Top_Depth_Real_v_predBy_NN1thick',
 'diff_TopTarget_DEPTH_v_rowDEPT',
 'diff_TopHelper_DEPTH_v_rowDEPT',
 'class_DistFrPick_TopHelper',
 'NewWell',
 'LastBitWell',
 'TopWellDept',
 'BotWellDept',
 'WellThickness',
    'rowsToEdge',
    'closTopBotDist',
    'closerToBotOrTop'
]

############## Next few lines to combine the two lists above and take those columns out of dataframe

def takeOutColNotNeededInTrainingDF(df,list_allCol,colToTakeOutCurves,colToTakeOutOther):
    print("number of columns in dataframe coming into function",len(df.columns))
    train_feats_minusLowCount = [x for x in list_allCol if x not in colToTakeOutCurves]
    train_feats_minusLowCount = [x for x in train_feats_minusLowCount if x not in colToTakeOutOther]
    df_train_featWithHighCount = df[train_feats_minusLowCount]
    print("number of columns in dataframe leaving function",len(df_train_featWithHighCount.columns))
    return df_train_featWithHighCount


df_train_featWithHighCount = takeOutColNotNeededInTrainingDF(df_all_Col_preSplit_wTrainTest_ClassBalanced,col_list,training_feats_w_lowCount,takeOutColumnsNotCurvesList)


list(df_train_featWithHighCount.columns)


##############  Number of columns for training
len(df_train_featWithHighCount.columns)

df_train_featWithHighCount.describe()

used_features = list(df_train_featWithHighCount.columns)
used_features 

#####################   Now let's take out those same columns in the test only dataframe
df_test_featWithHighCount = takeOutColNotNeededInTrainingDF(df_all_Col_test,col_list,training_feats_w_lowCount,takeOutColumnsNotCurvesList)

################ Now let's combine the rebalanced train df with the unrebalanced test df to make a df we will then split into 4 pieces: train-data, train-labels, test-data,test-lables
df_testPlusRebalTrain_featWithHighCount = pd.concat([df_train_featWithHighCount,df_test_featWithHighCount])
len(df_testPlusRebalTrain_featWithHighCount.columns)


# Identify which columns to use as labels
# The column 'cat_isTopMcMrNearby_known' is what we'll use as labels.

#     100 = exactly the Top McMurray Pick
#     95 if the distance between that depth and the Top McMurray Pick is -0.5 < x and x <0.5
#     60 if the distance between that depth and the Top McMurray Pick is -5 < x and x < 5
#     0 = not near the Top McMurray Pick

# The function used to make these classes or lables as column was: df_all_wells_wKNN_DEPTHtoDEPT['cat_isTopMcMrNearby_known']=df_all_wells_wKNN_DEPTHtoDEPT['diff_TMcM_Pick_v_DEPT'].apply(lambda x: 100 if x==0 else ( 95 if (-0.5 < x and x <0.5) else 60 if (-5 < x and x <5) else 0))

df_testPlusRebalTrain_featWithHighCount['class_DistFrPick_TopTarget'].unique()
labels = df_testPlusRebalTrain_featWithHighCount[['class_DistFrPick_TopTarget','UWI','trainOrTest','TopTarget_DEPTH']]

labels.head()

labels.tail()

len(labels)

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


#### split based on train in trainOrTest col
labels_train = labels[labels['trainOrTest'] == 'train' ]
#### Keep only the 'cat_isTopMcMrNearby_known' column, so now it is just a series of labels
labels_train = labels_train['class_DistFrPick_TopTarget']
#### split based on test in trainOrTest col
labels_test = labels[labels['trainOrTest'] == 'test' ]
#### Keep only the 'cat_isTopMcMrNearby_known' column, so now it is just a series of labels
labels_test = labels_test['class_DistFrPick_TopTarget']

df_train_featWithHighCount = df_testPlusRebalTrain_featWithHighCount

########################  Create training dataframes  ##################
#### split based on train in trainOrTest col and drop UWI and TrainOrTest columns
df_train_featWithHighCount_train = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount['trainOrTest'] == 'train' ].drop(columns=['UWI', 'trainOrTest','class_DistFrPick_TopTarget','TopTarget_DEPTH'])
#### split based on test in trainOrTest col and drop UWI and TrainOrTest columns
df_train_featWithHighCount_test = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount['trainOrTest'] == 'test' ].drop(columns=['UWI', 'trainOrTest','class_DistFrPick_TopTarget','TopTarget_DEPTH'])


##########3 Create index dataframes for reattaching'UWI', 'trainOrTest','class_DistFrPick_TopTarget','TopTarget_DEPTH'
df_train_featWithHighCount_train_indexOnly = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount['trainOrTest'] == 'train'][['UWI', 'trainOrTest','class_DistFrPick_TopTarget','TopTarget_DEPTH']]
df_train_featWithHighCount_test_indexOnly = df_testPlusRebalTrain_featWithHighCount[df_testPlusRebalTrain_featWithHighCount['trainOrTest'] == 'test' ][['UWI', 'trainOrTest','class_DistFrPick_TopTarget','TopTarget_DEPTH']]

df_train_featWithHighCount_train_indexOnly.head()

############## Rename to avoid overwriting & keep with previous work

train_X = df_train_featWithHighCount_train
train_y = labels_train
test_X = df_train_featWithHighCount_test
test_y = labels_test
train_index = df_train_featWithHighCount_train_indexOnly
test_index = df_train_featWithHighCount_test_indexOnly 

############### Inspect to make sure column headers and lengths make sense

print(len(train_X))
train_X.head()

print(len(train_y))
train_y.head()

print(len(test_X))
test_X.head()

print(len(test_y))
test_y.head()

########################################
# Save the dataframes as a dict

#     train_X
#     train_y
#     test_X
#     test_y
#     & full








###################### LOAD PREVIOUS CREATED DATASET WITH FEATURES ########################################################