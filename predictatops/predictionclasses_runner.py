# -*- coding: utf-8 -*-
# import predictionclasses 
# from configurationplusfiles_runner import input_data_inst, config, output_data_inst
# from main import getJobLibPickleResults



################## Load model & ML class instance from trainclasses step #############

# model = getJobLibPickleResults(output_data_inst,output_data_inst.path_trainclasses,"trainclasses_model.pkl")
# ML1 = getJobLibPickleResults(output_data_inst,output_data_inst.path_trainclasses,"trainclasses_ML1_instance.pkl")

model,ML1 =loadMLinstanceAndModel(output_data_inst)


print("the model imported is:",model)

################## Class Prediction Results for training dataframe for X #############

##### Creating a class_accuracy instance with the already established ML1 variable for an isntance of the ML_obj_class
ac = class_accuracy(ML1)


################## First with training data #############

#### Running the accuracy calculation using the model trained on training data against training data. 
#### Testing how well the model predicts the class of each point, with class being categorized distance from actual pick.
accuracy_train = ac.run_all(model,ac.train_X,ac.train_y,'TopTarget_Pick_pred','class_DistFrPick_TopTarget')

print("accuracy of training dataset",accuracy_train)


################## Then with test data ###############

#### Running the accuracy calculation using the model trained on training data against TEST data. 
#### Testing how well the model predicts the class of each point, with class being categorized distance from actual pick.
accuracy_test = ac.run_all(model,ac.test_X,ac.test_y,'TopTarget_Pick_pred','class_DistFrPick_TopTarget')

print("accuracy of test dataset",accuracy_test)


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


concatClass = InputDistClassPrediction_to_BestDepthForTop(output_data_inst)

concatClass.load_MLobj(ML1)

concatClass.help()

prediction_distClass_trainingData_ndarray = concatClass.predict_from_model(model,ML1.train_X)

concatClass1 = concatClass.concat_modelResultsNDArray_w_indexValues(concatClass.result_df_dist_class_prediction,"train",config.pick_class_str)


##### NEED TO PUT THIS LIST IN CONFIG ########## !!!!!!!
cols_to_keep_list = ['DEPT',"NN1_TopHelper_DEPTH","NN1_thickness","topTarget_Depth_predBy_NN1thick","DistFrom_NN1ThickPredTopDepth_toRowDept"]

concatClass2 = concatClass.concat_step2(ML1,"train",cols_to_keep_list)

#####
DEPTH_col_in_featureCreation = config.DEPTH_col_in_featureCreation
pick_class_str = config.pick_class_str
UWI = config.UWI
curve_windows_for_rolling_features = config.curve_windows_for_rolling_features
label_intergers = list(config.zonesAroundTops.keys())

distClassDF_wRollingCols_training = concatClass.calc_pred_vs_real_top_dif(concatClass.df_results_trainOrtest_wIndex,DEPTH_col_in_featureCreation,pick_class_str,UWI,curve_windows_for_rolling_features,label_intergers)


print("distClassDF_wRollingCols_training.head() = ",distClassDF_wRollingCols_training.head())

print("printing distClassDF_wRollingCols_training for checking that it makes sense::",distClassDF_wRollingCols_training.tail())

################ Now lets run test version   ################

concatClass_test = InputDistClassPrediction_to_BestDepthForTop(output_data_inst)


#####
DEPTH_col_in_featureCreation = config.DEPTH_col_in_featureCreation
pick_class_str = config.pick_class_str
UWI = config.UWI
curve_windows_for_rolling_features = config.curve_windows_for_rolling_features
label_intergers = list(config.zonesAroundTops.keys())



#### Doing it the 'all at once' way this time.
distClassDF_wRollingCols_testData = concatClass_test.run_all(ML1,model,"test",cols_to_keep_list,DEPTH_col_in_featureCreation,pick_class_str,UWI,curve_windows_for_rolling_features,label_intergers)

print("distClassDF_wRollingCols_testData.head()",distClassDF_wRollingCols_testData.head())

##################### The next part will attempt to go from classifiers of  ##################### 
#####################  (at, near, or far away from the pick in each well) to a single depth prediction for the pick in each well ###################### 
#####################  Class for calculating accuracy of single pick prediction in each well vs. #####################  
######################  known pick based on rolling average & median ranking of depths with distance class #####################  
#####################  predictions of being close to pick. #####################  

vs = {"depth_str":config.DEPTH_col_in_featureCreation,"pick_class_str":config.pick_class_str,"UWI_str" :config.UWI,"rollingWindows":config.curve_windows_for_rolling_features,"distClassIntegersArray" :list(config.zonesAroundTops.keys())}
print("vs",vs)
print("gap")
print("vs",vs["depth_str"])


#####################  Start accuracy_singleTopPerWellPrediction_fromRollingRules() class for training data  #####################  

rollToWell = accuracy_singleTopPerWellPrediction_fromRollingRules(ML1,vs,distClassDF_wRollingCols_training)

r2,mean_absolute_error_,df_calc_pred_Top_Pick_pred_DEPT_pred = rollToWell.run_all('TopTarget_Pick_pred_DEPT_pred','TopTarget_DEPTH',keepAllWells="yes",dropIfOnlyClasses=[0])


print("len(df_calc_pred_Top_Pick_pred_DEPT_pred",len(df_calc_pred_Top_Pick_pred_DEPT_pred))
print("r2 of training dataset in terms of pick depths = ",r2)
print("mean_absolute_error_ of training dataset in terms of pick depths = ",mean_absolute_error_)

print("percent of wells kept because they weren't just class zero in rollToWell function for training:",rollToWell.precentWellsKept)

#####################  Now accuracy for test dataset again via accuracy_singleTopPerWellPrediction_fromRollingRules()  #####################  

#####################  First we'll do it and keep all wells not matter whether or not they include any class predictions other than zero  #####################  
#####################  This will include some wells with some very bad predictions as there are not class predictions to go off of #####################  


rollToWell_test = accuracy_singleTopPerWellPrediction_fromRollingRules(ML1,vs,distClassDF_wRollingCols_testData)
r2_test,mean_absolute_error_test,df_calc_pred_Top_Pick_pred_DEPT_pred2 = rollToWell_test.run_all('TopTarget_Pick_pred_DEPT_pred','TopTarget_DEPTH',keepAllWells="yes",dropIfOnlyClasses=[0])

print("r2 for test and all wells kept is:",r2_test)
print("mean_absolute_error_test for test and all wells kept is:",mean_absolute_error_test)
print("percent wells kept for test and all wells kept is:",rollToWell_test.precentWellsKept)

#####################  Now let's try it for test dataset but exclude wells that only have a zero class prediction #####################  

rollToWell_test_NoZeros = accuracy_singleTopPerWellPrediction_fromRollingRules(ML1,vs,distClassDF_wRollingCols_testData)
r2_test_NoZeros ,mean_absolute_error_test_NoZeros ,df_calc_pred_Top_Pick_pred_DEPT_pred2_NoZeros  = rollToWell_test_NoZeros .run_all('TopTarget_Pick_pred_DEPT_pred','TopTarget_DEPTH',keepAllWells="no",dropIfOnlyClasses=[0])

print("r2 for test and wells excluded that only had zero class predicted is:",r2_test_NoZeros)
print("mean_absolute_error_test for test and wells excluded that only had zero class predicted is:",mean_absolute_error_test_NoZeros)
print("percent wells kept for test and wells excluded that only had zero class predicted is:",rollToWell_test_NoZeros.precentWellsKept)

number_of_wells_thrown_out = len(rollToWell_test_NoZeros.fullUWIsSet) - len(rollToWell_test_NoZeros.fullUWIsSet)*rollToWell_test_NoZeros.precentWellsKept

print("number of wells with only zeros predicted that were thrown out:",number_of_wells_thrown_out)


