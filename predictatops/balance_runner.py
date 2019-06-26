# -*- coding: utf-8 -*-

################ import from other python files in this package ###################
from balance import *
from configurationplusfiles_runner import input_data_inst, config, output_data_inst

##### BASED ON notebook PreML_ClassRebalence_FeatureSelection_Prep_20181003_vF in Mannville repo
##### preceeded by feature creation notebooks
##### (without Dask)


######################  Purpose is to duplicate some of the rows near the pick so they are more common  ######################
######################  and take out some of the rows farther away in training dataset, so they are less common  ######################
###################### This will REBALANCE the classes in the dataset ##################################################################


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


# #### Had to change display options to get this to print in full!
# #pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.options.display.max_colwidth = 100000


################# LOAD DATA RESULTS FROM FEATURE CREATION STEP PREVIOUSLY ##############
features_df_results = get_features_df_results(output_data_inst)

df_all_Col_train_noRebalance, df_all_Col_test = takeInDFandSplitIntoTrainTestDF(
    features_df_results, config
)


##### Rebalance class, aka label, populations to deal with lopsided class populations
##### Because we have a lot more rows far away from the pick than exactly at the pick or close to the pick, we run the risk of being class heavy in some areas. This can result in not enough ability to identify the sparsely populate classes, like right at the pick.
##### We'll attemp to deal with this problem by throwing out some of the rows far away from the pick and duplicating some of the rows right at or near the pick.
##### THIS SHOULD ONLY BE DONE TO THE TRAINING DATA NOT THE TEST DATA OR THAT IS CHEATING!

class_array_NearPick = getListOfKeysForZonesObj(config)

test_df_return = countRowsByClassOfNearPickOrNot(
    df_all_Col_test, class_array_NearPick, 2, 0
)

#### prints some info for checking the populations of the classes
df_all_Col_preSplit_wTrainTest_ClassBalanced = dropsRowsWithMatchClassAndDeptRemainderIsZero(
    df_all_Col_train_noRebalance, "class_DistFrPick_TopTarget", 7, 0
)

#### prints some info for checking the populations of the classes
df_all_Col_preSplit_wTrainTest_ClassBalanced.info()

#### now we duplicate some rows for the class that wasn't well populated.
## df_all_Col_preSplit_wTrainTest_ClassBalanced2 = addsRowsToBalanceClasses(df_all_Col_preSplit_wTrainTest_ClassBalanced,50,10)
df_all_Col_preSplit_wTrainTest_ClassBalanced2 = addsRowsToBalanceClasses(
    df_all_Col_preSplit_wTrainTest_ClassBalanced,
    config.rebalanceClassZeroMultiplier,
    config.rebalanceClass95Multiplier,
)

#### Prints some status on : findNumberOfEachClass
findNumberOfEachClass(
    df_all_Col_preSplit_wTrainTest_ClassBalanced2, "class_DistFrPick_TopTarget"
)
print(len(df_all_Col_preSplit_wTrainTest_ClassBalanced2))

print(df_all_Col_preSplit_wTrainTest_ClassBalanced2.info())

df_all_Col_preSplit_wTrainTest_ClassBalanced = (
    df_all_Col_preSplit_wTrainTest_ClassBalanced2
)

#### printing a list of all the columns that we will use further down.
col_list = list(df_all_Col_preSplit_wTrainTest_ClassBalanced.columns)
print("col_list in module balance_runner.py", col_list)


#### We'll now exclude two lists of columns before going further! ##############3
columns_to_not_trainOn_andNotCurves = config.columns_to_not_trainOn_andNotCurves
columns_to_not_trainOn_andAreCurves = config.columns_to_not_trainOn_andAreCurves

##### NOTE: BUT LEAVE IN THE 'class_DistFrPick_TopTarget' column for now as thats a label we'll use in label df!!!! ####

############ Next few lines to combine the two lists above and take those columns out of dataframe ###########

training_feats_w_lowCount = config.columns_to_not_trainOn_andAreCurves
takeOutColumnsNotCurvesList = config.columns_to_not_trainOn_andNotCurves

df_train_featWithHighCount = takeOutColNotNeededInTrainingDF(
    df_all_Col_preSplit_wTrainTest_ClassBalanced,
    col_list,
    training_feats_w_lowCount,
    takeOutColumnsNotCurvesList,
)


print(
    "list(df_train_featWithHighCount.columns) - Are these columns we want to continue having for training?",
    list(df_train_featWithHighCount.columns),
)
print(
    "len(df_train_featWithHighCount.columns)", len(df_train_featWithHighCount.columns)
)

## df_train_featWithHighCount.describe()

used_features = list(df_train_featWithHighCount.columns)

########### Now let's take out those same columns in the test only dataframe ###########

df_test_featWithHighCount = takeOutColNotNeededInTrainingDF(
    df_all_Col_test, col_list, training_feats_w_lowCount, takeOutColumnsNotCurvesList
)

########### Now let's combine the rebalanced train df with the unrebalanced test df to make a df we will then split into 4 pieces: train-data, train-labels, test-data,test-lables ##########
df_testPlusRebalTrain_featWithHighCount = combineRebalancedTrainDFWithUnrebalancedTestDF(
    df_train_featWithHighCount, df_test_featWithHighCount
)


######## Identify which columns to use as labels ########
# The column 'cat_isTopMcMrNearby_known' is what we'll use as labels.

#     100 = exactly the Top McMurray Pick
#     95 if the distance between that depth and the Top McMurray Pick is -0.5 < x and x <0.5
#     60 if the distance between that depth and the Top McMurray Pick is -5 < x and x < 5
#     0 = not near the Top McMurray Pick

# The function used to make these classes or lables as column was: df_all_wells_wKNN_DEPTHtoDEPT['cat_isTopMcMrNearby_known']=df_all_wells_wKNN_DEPTHtoDEPT['diff_TMcM_Pick_v_DEPT'].apply(lambda x: 100 if x==0 else ( 95 if (-0.5 < x and x <0.5) else 60 if (-5 < x and x <5) else 0))

df_testPlusRebalTrain_featWithHighCount["class_DistFrPick_TopTarget"].unique()
labels = df_testPlusRebalTrain_featWithHighCount[
    ["class_DistFrPick_TopTarget", "UWI", "trainOrTest", "TopTarget_DEPTH"]
]

labels.head()

labels.tail()

len(labels)


# df_testPlusRebalTrain_featWithHighCount['class_DistFrPick_TopTarget'].unique()

# columns_to_use_as_labels = config.columns_to_use_as_labels  ##### ['class_DistFrPick_TopTarget','UWI','trainOrTest','TopTarget_DEPTH']

##### Get dataframe of just the labels!  ###########
# labels = df_testPlusRebalTrain_featWithHighCount[columns_to_use_as_labels]

labels = makeDFofJustLabels(df_testPlusRebalTrain_featWithHighCount, config)


##############     Now separate into 4 dataframes =    ###########
# train_labels
# train_feat
# test_labels
# test_feat

df_testPlusRebalTrain_featWithHighCount, train_X, train_y, test_X, test_y, train_index, test_index = make4separateDF(
    labels, df_testPlusRebalTrain_featWithHighCount, config
)

# Then take off UWI and TrainTest col <= check that this was done??????


#### Save Results to Locatino Established in : output_data_inst
saveRebalanceResultsAsHDF(
    df_testPlusRebalTrain_featWithHighCount,
    train_X,
    train_y,
    test_X,
    test_y,
    train_index,
    test_index,
    output_data_inst,
)
