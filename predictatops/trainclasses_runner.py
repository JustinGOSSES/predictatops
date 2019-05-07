# -*- coding: utf-8 -*-


################ import from other python files in this package ###################
from wellsKNN import *
from configurationplusfiles_runner import input_data_inst, config, output_data_inst

## pandas Options to be run so everything displays properly
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.options.display.max_colwidth = 100000

#### Optional checks
# print(welly.__version__)
# print(dask.__version__)
# print(pd.__version__)
# 0.3.5
# 0.18.2
# 0.23.3


###### LOAD RESULTS DATAFRAME IN HD5 FROM BALANCE PORTION OF WORKFLOW ###########

##### OLD STYLE #########

# knn_dir = "../WellsKNN/"
# load_dir = "../loadLAS"
# features_dir = "../createFeatures/"
# machine_learning_dir = "../Pre_ML_Rebalance_Splitting/"
# h5_to_load = 'df_all_Col_preSplit_wTrainTest_ClassBalanced_PreML_20181003.h5'

# ML1 = ML_obj_class(knn_dir,load_dir,features_dir,machine_learning_dir,h5_to_load )

# ML1.knn_dir

# ML1.load_data_for_ml()

# ML1.preSplitpreBal.head()

model = ML1.init_XGBoost_withSettings()

############ just to show what model contains a bit  ###########

print("just to show what model contains a bit:")

print("type(model)",type(model))

print("model stats",model)

print("model.subsample",model.subsample)

############   Optionally loading the already trained model here if it already exists locally.   ############ 
############   It can take quite a while to fit the model, so sometimes easier to save a copy and then load it.   ############ 

######################### WRITE FUNCTION FOR THIS !!!!!! ####################
######################### Something like: model = pickle.load(open("classModel_20181122a.pickle.dat", "rb")) & print(type(model))




################## Class Prediction Results for training dataframe for X #############

##### Creating a class_accuracy instance with the already established ML1 variable for an isntance of the ML_obj_class
ac = class_accuracy(ML1)

################## First with training data #############

#### Running the accuracy calculation using the model trained on training data against training data. 
#### Testing how well the model predicts the class of each point, with class being categorized distance from actual pick.
accuracy = ac.run_all(model,ac.train_X,ac.train_y,'TopTarget_Pick_pred','class_DistFrPick_TopTarget')

print("accuracy of training dataset",accuracy)

################## Then with test data ###############

#### Running the accuracy calculation using the model trained on training data against TEST data. 
#### Testing how well the model predicts the class of each point, with class being categorized distance from actual pick.
accuracy = ac.run_all(model,ac.test_X,ac.test_y,'TopTarget_Pick_pred','class_DistFrPick_TopTarget')

print("accuracy of test dataset",accuracy)


####################################### THIS IS TEST FOR ACCURACY OVER ALL ROWS, WHICH WE REALLY DON"T CARE ABOUT ##########
############ WE CARE ABOUT THE PICK ############################

# New class for functions that take in point by point distance class prediction and use rolling window and other methods to pick which point should be the top in question
# Make a few different columns classifiers that get the rolling mean of pick classifiers within different windows.
# This will help compare a class prediction of 95 in one part of the well to a class prediction of 95 in a nother part of the well. The assumption being the right prediction will have not just one 100 or 95 prediction but several in close proximity where as the false predictions are more likely to be by themselves:

#     Median
#     Rolling mean 6
#     Rolling mean 12
#     Rolling Mean 20
#     Sums of rolling all means


concatClass = InputDistClassPrediction_to_BestDepthForTop()

concatClass.load_MLobj(ML1)

concatClass.help()

prediction_distClass_trainingData_ndarray = concatClass.predict_from_model(model,ML1.train_X)

concatClass1 = concatClass.concat_modelResultsNDArray_w_indexValues(concatClass.result_df_dist_class_prediction,"train",vs.pick_class_str)

##### NEED TO PUT THIS LIST IN CONFIG ########## !!!!!!!
cols_to_keep_list = ['DEPT',"NN1_TopHelper_DEPTH","NN1_thickness","topTarget_Depth_predBy_NN1thick","DistFrom_NN1ThickPredTopDepth_toRowDept"]

concatClass2 = concatClass.concat_step2(ML1,"train",cols_to_keep_list)

distClassDF_wRollingCols_training = concatClass.run_all(concatClass.df_results_trainOrtest_wIndex,vs.depth_str,vs.pick_class_str,vs.UWI_str,vs.rollingWindows,vs.distClassIntegersArray)

print("distClassDF_wRollingCols_training.head() = ",distClassDF_wRollingCols_training.head())

####### or run the full thing at once
#  distClassDF_wRollingCols_training2 = concatClass.run_all(ML1,model,"train",vs,cols_to_keep_list,concatClass.df_results_trainOrtest_wIndex,vs.depth_str,vs.pick_class_str,vs.UWI_str,vs.rollingWindows,vs.distClassIntegersArray)

#print("distClassDF_wRollingCols_training2.head()",distClassDF_wRollingCols_training2.head())

################ Now lets run test version   ################

concatClass_test = InputDistClassPrediction_to_BestDepthForTop()

#### Doing it the 'all at once' way this time.
distClassDF_wRollingCols_testData = concatClass_test.run_all(ML1,model,"test",vs,cols_to_keep_list,vs.depth_str,vs.pick_class_str,vs.UWI_str,vs.rollingWindows,vs.distClassIntegersArray)

print("distClassDF_wRollingCols_testData.head()",distClassDF_wRollingCols_testData.head())

##################### The next part will attempt to go from classifiers of  ##################### 
#####################  (at, near, or far away from the pick in each well) to a single depth prediction for the pick in each well ###################### 
#####################  Class for calculating accuracy of single pick prediction in each well vs. #####################  
######################  known pick based on rolling average & median ranking of depths with distance class #####################  
#####################  predictions of being close to pick. #####################  


### Start accuracy_singleTopPerWellPrediction_fromRollingRules() class for training data ####

rollToWell = accuracy_singleTopPerWellPrediction_fromRollingRules(ML1,vs,distClassDF_wRollingCols_training)
r2,mean_absolute_error_,df_calc_pred_Top_Pick_pred_DEPT_pred = rollToWell.run_all('TopTarget_Pick_pred_DEPT_pred','TopTarget_DEPTH')

print("len(df_calc_pred_Top_Pick_pred_DEPT_pred",len(df_calc_pred_Top_Pick_pred_DEPT_pred)

print("r2 of training dataset in terms of pick depths = ",r2)
print("mean_absolute_error_ of training dataset in terms of pick depths = ",mean_absolute_error_)

print("len(train_list)",len(train_list))

test_list_short = []
for item in test_list:
    if item > 3:
        test_list_short.append(item)
len(test_list_short)

############### Now TEST data version ###############

rollToWell_test = accuracy_singleTopPerWellPrediction_fromRollingRules(ML1,vs,distClassDF_wRollingCols_testData)
r2_testData,mean_absolute_error_testData,df_calc_pred_Top_Pick_pred_DEPT_pred_testData = rollToWell_test.run_all('TopTarget_Pick_pred_DEPT_pred','TopTarget_DEPTH')


print("r2 of test dataset in terms of pick depths = ",r2_testData)
print("mean_absolute_error_ of test dataset in terms of pick depths = ",mean_absolute_error_testData)

############### The prediction are off in large part because a few wells have no ############### 
################ prediction at all, which is treated as a zero! In real life, we would happily ############### 
################  know we can't predict those wells with this model (by virtue of getting a zero ############### 
################  for them) and ignore them, so let's use that in our stats too! ############### 

print("next bit is This is accuracy of prediction for each well of test dataset but excludes the few wells that only have zeros predicted for distance class at every point!!")

rollToWell_test_noZeros = accuracy_singleTopPerWellPrediction_fromRollingRules(ML1,vs,distClassDF_wRollingCols_testData)

r2_testData_NoZeros,mean_absolute_error_testData_NoZeros,df_calc_pred_Top_Pick_pred_DEPT_pred_testData_NoZeros = rollToWell_test_noZeros.run_all('TopTarget_Pick_pred_DEPT_pred','TopTarget_DEPTH',keepAllWells="yes",dropIfOnlyClasses=[0])

r2_testData_NoZeros

print("r2 of test dataset without few wells we know will be incorrect without seeing answer in terms of pick depths = ",r2_testData_NoZeros)
print("mean_absolute_error_ r2 of test dataset without few wells we know will be incorrect without seeing answer in terms of pick depths = ",mean_absolute_error_testData_NoZeros)
print("The percent of the wells kept is : ",rollToWell_test_noZeros.precentWellsKept)





