# -*- coding: utf-8 -*-


################ imports ###################
import pandas as pd
import numpy as np
import itertools

# import matplotlib.pyplot as plt
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
from dask.distributed import Client
import random
from xgboost.sklearn import XGBClassifier
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import multiprocessing

from main import getJobLibPickleResults

#### Adding this bit to silence an error that was causing the notebook to have a dead kernal
#### This is an unsafe solution but couldn't get any  of the "right solutions" to work!
#### Ended up using this = https://www.kaggle.com/c/bosch-production-line-performance/discussion/25082
#### Other solutions = https://github.com/dmlc/xgboost/issues/1715 but the solution here didn't seem to work for me?
import os

# os.environ['KMP_DUPLICATE_LIB_OK']='True'

###### Set environment variable to get around weird conda clang error that causes notebook kernal to die. ########
###### Error was: OMP: Error #15: Initializing libomp.dylib, but found libiomp5.dylib already initialized.
###### OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://openmp.llvm.org/
###### Abort trap: 6
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


################## Class Prediction Results for training dataframe for X #############
def loadMLinstanceAndModel(output_data_inst):
    model = getJobLibPickleResults(
        output_data_inst, output_data_inst.path_trainclasses, "trainclasses_model.pkl"
    )
    ML1 = getJobLibPickleResults(
        output_data_inst,
        output_data_inst.path_trainclasses,
        "trainclasses_ML1_instance.pkl",
    )
    return model, ML1


class class_accuracy:
    """
    This class holds several functions for calculating accuracy of the class-identification model
    It takes in as the initiation argument, an instance of the ML_obj_class, which contains all the 
    necessary data already processed with features created and ready to do for the machine-learning task.
    It initiates on creation a variety of class instance attributes that mirror those created in the ML_obj_class class.
    There are 5 functions. The help function will print some explanitory text. 
    The rest proceed to predict a dataframe from a trained model, reformat some of the input data so
    it can be combined, calculate accuracy, and a final function that runs the last three if you don't want to
    run them individually. 
    The last two functions will return an accuracy nubmer as a percentage of class rows or instances the model predicted corrected.
    
    """

    def __init__(self, ML):
        # self.knn_dir = ML.knn_dir
        # self.load_dir = ML.load_dir
        # self.features_dir = ML.features_dir
        self.machine_learning_dir = ML.machine_learning_dir
        self.h5_to_load = ML.h5_to_load
        self.train_X = ML.train_X
        self.train_y = ML.train_y
        self.test_X = ML.test_X
        self.test_y = ML.test_y
        self.train_index = ML.train_index
        self.test_index = ML.test_index
        self.preSplitpreBal = ML.preSplitpreBal
        self.result_df_from_prediction = None

    def help(self):
        print(
            " eventually there will some sort of help printed here to explain this function more and how it is envisioned you wil run it. In other words, step 1, step 2, etc."
        )

    def predict_from_model(self, model, df_X_toPredict):
        """
        The predict_from_model function takes as argument a model that is already trained on training data, in the demo case a 
        scikit-learn XGBoost model and the dataframe of the columns to predict. From this, it fills in 
        the self.result_df_from_prediction attribute and returns nothing.
    
        """
        self.result_df_from_prediction = model.predict(df_X_toPredict)

    def first_Reformat(self, train_y, TopTarget_Pick_pred):
        train_y_indexValues = train_y.index.values
        df_result_train = pd.DataFrame(
            self.result_df_from_prediction,
            index=train_y_indexValues,
            columns=[TopTarget_Pick_pred],
        )
        df_results_train_ = pd.concat([train_y, df_result_train], axis=1)
        return df_results_train_

    def accuracy_calc(self, train_y, TopTarget_Pick_pred, class_DistFrPick_TopTarget):
        df_results_train_ = self.first_Reformat(train_y, TopTarget_Pick_pred)
        accuracy = accuracy_score(
            df_results_train_[class_DistFrPick_TopTarget],
            df_results_train_[TopTarget_Pick_pred],
        )
        return accuracy

    def run_all(
        self,
        model,
        df_X_toPredict,
        train_y,
        TopTarget_Pick_pred,
        class_DistFrPick_TopTarget,
    ):
        self.predict_from_model(model, df_X_toPredict)
        return self.accuracy_calc(
            train_y, TopTarget_Pick_pred, class_DistFrPick_TopTarget
        )


#### Example of use of function above:
##### Creating a class_accuracy instance with the already established ML1 variable for an isntance of the ML_obj_class
# ac = class_accuracy(ML1)

################## Class Prediction Results for training dataframe for X #############

##### Creating a class_accuracy instance with the already established ML1 variable for an isntance of the ML_obj_class
# ac = class_accuracy(ML1)

################## First with training data #############

#### Running the accuracy calculation using the model trained on training data against training data.
#### Testing how well the model predicts the class of each point, with class being categorized distance from actual pick.
# accuracy = ac.run_all(model,ac.train_X,ac.train_y,'TopTarget_Pick_pred','class_DistFrPick_TopTarget')

# print("accuracy of training dataset",accuracy)

################## Then with test data ###############

#### Running the accuracy calculation using the model trained on training data against TEST data.
#### Testing how well the model predicts the class of each point, with class being categorized distance from actual pick.
# accuracy = ac.run_all(model,ac.test_X,ac.test_y,'TopTarget_Pick_pred','class_DistFrPick_TopTarget')

# print("accuracy of test dataset",accuracy)

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

########  In the future, it would be nice to calculate error bars as well!!!!!    ##########


##################### The next part will attempt to go from classifiers of  #####################
#####################  (at, near, or far away from the pick in each well) to a single depth prediction for the pick in each well ######################
#####################  Class for calculating accuracy of single pick prediction in each well vs. #####################
######################  known pick based on rolling average & median ranking of depths with distance class #####################
#####################  predictions of being close to pick. #####################


class InputDistClassPrediction_to_BestDepthForTop:
    """
    Explain theyself
    """

    def __init__(self, output_data_inst):
        self.result_df_dist_class_prediction = None
        self.concat_modelResults_w_indexValues = None
        self.df_results_trainOrtest_wIndex = None
        self.model = None
        self.MLobj = None
        self.result_df_dist_class_prediction = None

    def help(self):
        print(
            " eventually there will some sort of help printed here to explain this function more and how it is envisioned you wil run it. In other words, step 1, step 2, etc."
        )

    def load_MLobj(self, MLobj):
        self.MLobj = MLobj
        print("loaded model into object instance")

    def predict_from_model(self, model, df_X_toPredict):
        """
        The predict_from_model function takes as argument a model that is already trained on training data, in the demo case a 
        scikit-learn XGBoost model and the dataframe of the columns to predict. From this, it fills in 
        the self.result_df_from_prediction attribute and returns nothing.
    
        """
        self.result_df_dist_class_prediction = model.predict(df_X_toPredict)
        if type(self.result_df_dist_class_prediction) == None:
            print(
                "this function didn't work, self.distClassDF_wRollingCols_training is not populated with anything but None"
            )
        else:
            print(
                "ran predict_from_model() which runs inside self.result_df_dist_class_prediction = model.predict(df_X_toPredict) access the results by appending .result_df_dist_class_prediction to the class instance"
            )
        return self.result_df_dist_class_prediction

    def load_dist_class_pred_df(self, dist_class_pred_df):
        """
        explain theyself
        """
        #         if self.result_df_dist_class_prediction == None:
        self.result_df_dist_class_prediction = dist_class_pred_df

    #         else:
    #             print("trying to replace earlier result_df_dist_class_prediction")

    def concat_modelResultsNDArray_w_indexValues(
        self, distClassModel_resultsNDArry, train_or_test, col_name_prediction
    ):
        #### self,self.result_df_dist_class_prediction,"test",vs.pick_class_str
        if train_or_test == "train":
            y_indexValues = self.MLobj.train_y.index.values
            train_or_test_y = self.MLobj.train_y
        else:
            y_indexValues = self.MLobj.test_y.index.values
            train_or_test_y = self.MLobj.test_y
        print(type(distClassModel_resultsNDArry))
        print(type(y_indexValues))
        if len(distClassModel_resultsNDArry) != len(y_indexValues):
            print(
                "Two input arguments length does not match. This invalidates an assumption of this function"
            )
            print(
                "length of distClassModel_resultsNDArry is ",
                len(distClassModel_resultsNDArry),
                " and length of y_indexValues",
                len(y_indexValues),
            )
        else:
            # y_indexValues = train_or_test_y.index.values
            # df_result = pd.DataFrame(result_test, index=test_y_indexValues, columns=['TopTarget_Pick_pred'])
            df_result = pd.DataFrame(
                distClassModel_resultsNDArry,
                index=y_indexValues,
                columns=[col_name_prediction],
            )
            df_results_test_ = pd.concat([train_or_test_y, df_result], axis=1)
            self.concat_modelResults_w_indexValues = df_results_test_
            return self.concat_modelResults_w_indexValues

    def concat_step2(self, MLobj, train_or_test, cols_to_keep_list):
        #### cols_to_keep_list = ['DEPT',"NN1_TopHelper_DEPTH","NN1_thickness","topTarget_Depth_predBy_NN1thick","DistFrom_NN1ThickPredTopDepth_toRowDept"]
        if train_or_test == "train":
            TrainOrTest_index = MLobj.train_index
            df_ = self.MLobj.train_X
        else:
            TrainOrTest_index = MLobj.test_index
            df_ = self.MLobj.test_X
        df_results_test_ = self.concat_modelResults_w_indexValues
        df_results_test_wIndex = pd.concat(
            [df_results_test_, TrainOrTest_index], axis=1
        )
        df_results_test_wIndex2 = pd.concat(
            [df_results_test_wIndex, df_[cols_to_keep_list]], axis=1
        )
        self.df_results_trainOrtest_wIndex = df_results_test_wIndex2
        print(
            "in concat_step2, type of df_results_trainOrtest_wIndex=",
            type(self.df_results_trainOrtest_wIndex),
        )
        return self.df_results_trainOrtest_wIndex

    def calc_pred_vs_real_top_dif(
        self, df, depth_str, pick_pred_class_str, UWI_str, rollingWindows, predClasses
    ):
        """
        Function takes in:
            A dataframe with predictions and dataframe with UWIs and known pick depths. Dataframes may not be same length but df 2 must have all UWIs in df 1.
        Function returns:
            A column for predicted dataframe with calculated single prediction depth pick based on the median row technique
            A column for predicted dataframe with calculated single prediction depth pick based on rolling means of classes predicted for each row.
        THESE BELOW ARE NOTE YET IMPLIMENTED!    
            A new dataframe that is just one row per well and includes as col of UWIs, known picks, predicted picks, and difference
            A new col in the new df that has high and low error by some metric?
            A score of mean abosolute error across all wells in the given dataframe 1.
        """

        df_merges = df.copy()
        all_new_rolling_mean_col = []
        for Window in rollingWindows:
            new_col = pick_pred_class_str + "_classRollMean" + str(Window)
            all_new_rolling_mean_col.append(new_col)
            half_window_neg = -1 * math.floor(Window / 2)
            df_merges[new_col] = (
                df_merges.groupby([UWI_str])[pick_pred_class_str]
                .shift(half_window_neg)
                .rolling(Window)
                .mean()
                .fillna(0)
            )
        df_merges[pick_pred_class_str + "classRollMeanSum"] = 0
        for col in all_new_rolling_mean_col:
            df_merges[pick_pred_class_str + "classRollMeanSum"] += df_merges[col]
        df_merges[pick_pred_class_str + "classRollMeanSum"] += df_merges[
            pick_pred_class_str
        ].astype(float)
        idx = df_merges.loc[
            df_merges.groupby(["UWI"])[
                pick_pred_class_str + "classRollMeanSum"
            ].idxmax()
        ]
        # print('idx=',idx)
        print("type(idx)", type(idx))
        #     print(idx[['UWI','DEPT',pick_pred_class_str+'classRollMeanSum']])
        max_frame = idx[["UWI", "DEPT", pick_pred_class_str + "classRollMeanSum"]]
        max_frame.columns = [
            "UWI",
            pick_pred_class_str + "_DEPT_pred",
            pick_pred_class_str + "_classRollMeanSum",
        ]
        # print("type",type(max_series),"and max series is ",max_series)
        df_merges = pd.merge(df_merges, max_frame, on="UWI", how="outer")
        return df_merges

        # ML1,model,"test",         vs,cols_to_keep_list,concatClass_test.df_results_trainOrtest_wIndex,vs.depth_str,vs.pick_class_str,vs.UWI_str,vs.rollingWindows,vs.distClassIntegersArray

    def run_all(
        self,
        MLobj,
        model,
        trainOrTest_str,
        cols_to_keep_list,
        depth_str,
        pick_pred_class_str,
        UWI_str,
        rollingWindows,
        predClasses,
    ):
        """
        Runs two functions. Takes in first the resulting dataframe from model.predict(df_X_toPredict). Take in second, depth_str,pick_pred_class_str,UWI_str,rollingWindows,predClasses.
        Creates rolling means and median distance class values across different size rolling windows.
        """
        ##
        self.load_MLobj(MLobj)
        if trainOrTest_str == "train":
            self.predict_from_model(model, MLobj.train_X)
        else:
            self.predict_from_model(model, MLobj.test_X)
        # self.load_dist_class_pred_df(dist_class_pred_df)
        self.concat_modelResultsNDArray_w_indexValues(
            self.result_df_dist_class_prediction, trainOrTest_str, pick_pred_class_str
        )
        self.concat_step2(MLobj, trainOrTest_str, cols_to_keep_list)

        ##
        dist_class_pred_df = self.df_results_trainOrtest_wIndex
        print("type of dist_class_pred_df", type(dist_class_pred_df))
        print(
            "type of self.df_results_trainOrtest_wIndex",
            type(self.df_results_trainOrtest_wIndex),
        )

        df_merges = self.calc_pred_vs_real_top_dif(
            self.df_results_trainOrtest_wIndex,
            depth_str,
            pick_pred_class_str,
            UWI_str,
            rollingWindows,
            predClasses,
        )
        return df_merges


class accuracy_singleTopPerWellPrediction_fromRollingRules:
    """
    stuff here
    calculates accuracy on a per well basis after doing some rolling mean analysis on per depth point scores from machine-learning classification of distance class.
    """

    from sklearn.metrics import mean_absolute_error

    def __init__(self, ML, vs, distClassDF_wRollingCols_training):
        # self.knn_dir = ML.knn_dir
        # self.load_dir = ML.load_dir
        # self.features_dir = ML.features_dir
        # self.machine_learning_dir = ML.machine_learning_dir
        # self.h5_to_load = ML.h5_to_load
        self.train_X = ML.train_X
        self.train_y = ML.train_y
        self.test_X = ML.test_X
        self.test_y = ML.test_y
        self.train_index = ML.train_index
        self.test_index = ML.test_index
        self.preSplitpreBal = ML.preSplitpreBal
        self.result_df_from_prediction = None  # df
        ####
        ####
        self.vs = vs  # object instance from variables class
        self.depth_str = vs["depth_str"]
        self.pick_class_str = vs["pick_class_str"]
        self.UWI_str = vs["UWI_str"]
        self.rollingWindows = vs["rollingWindows"]
        self.distClassIntegersArray = vs["distClassIntegersArray"]
        ####
        self.calc_pred = distClassDF_wRollingCols_training
        self.excludeWellsThatOnlyHaveTheseClasses = (
            []
        )  ### aka dropIfOnlyClasses in optionallyExcludeWellsWithoutStrongPredictions()
        self.NoGoodWellsToExclude = (
            []
        )  #### UWIs of wells that only had zeros in the predicted dsitance class so these wells were excluded from accurracy prediction
        ####
        self.calc_pred_TopMcMr_Pick_pred_DEPT_pred = None  # df
        self.calc_pred_TopTarget_DEPTH = None  # df
        self.fullUWIsSet = []  ### set of UWIs in the dataframe
        self.precentWellsKept = 1
        self.UWIsSetSubsetKept = (
            []
        )  #### subset of the wells that have predictions that aren't just zero or something else not wanted

    ## if zeros, calc_pred is changed to without zeros and zerosExcluded Array is populated

    def help(self):
        print(
            " eventually there will some sort of help printed here to explain this function more and how it is envisioned you wil run it. In other words, step 1, step 2, etc."
        )

    def load_variables_obj(vs):
        # vs.depth_str,vs.pick_class_str,vs.UWI_str
        self.vs = vs
        print("variables loaded include:", list(vs.keys()))

    def optionallyExcludeWellsWithoutStrongPredictions(
        self, keepAllWells=None, dropIfOnlyClasses=[0]
    ):
        # [0,60,70,95,100]
        self.excludeWellsThatOnlyHaveTheseClasses = dropIfOnlyClasses
        if keepAllWells == "no":
            calc_pred = self.calc_pred
            self.fullUWIsSet = calc_pred[self.UWI_str].unique()
            for eachClass in dropIfOnlyClasses:
                calc_pred = calc_pred.loc[
                    calc_pred["TopTarget_Pick_pred_classRollMeanSum"] != eachClass
                ]
            # calc_pred_noZeros = calc_pred.loc[calc_pred['TopTarget_Pick_pred_classRollMeanSum'] != 0]
            self.UWIsSetSubsetKept = calc_pred[self.UWI_str].unique()

            self.calc_pred = calc_pred
            print("hit yes in optionallyExcludeWellsWithoutStrongPredictions()")
        else:
            calc_pred = self.calc_pred
            self.fullUWIsSet = calc_pred[self.UWI_str].unique()
            self.UWIsSetSubsetKept = calc_pred[self.UWI_str].unique()
            # uniqueVals = df["cluster"].unique()
            print("hit pass in optionallyExcludeWellsWithoutStrongPredictions()")
        self.precentWellsKept = len(self.UWIsSetSubsetKept) / len(self.fullUWIsSet)

    def reduceDFtoOneBestTopPredictionPerWell(self, TopTarget_Pick_pred_DEPT_pred):
        ## TopTarget_Pick_pred_DEPT_pred = 'TopTarget_Pick_pred_DEPT_pred'
        """
        THINGS GO HERE
        """
        self.TopTarget_Pick_pred_DEPT_pred = TopTarget_Pick_pred_DEPT_pred
        df = self.calc_pred
        self.calc_pred_Top_Pick_pred_DEPT_pred = (
            df.groupby([self.UWI_str])[TopTarget_Pick_pred_DEPT_pred]
            .mean()
            .to_frame()
            .reset_index()
        )

    def reduceDFtoOriginalTopPerWell(self, TopTarget_DEPTH):
        ## TopTarget_DEPTH = 'TopTarget_DEPTH'
        """
        THINGS GO HERE
        """
        df = self.calc_pred
        self.TopTarget_DEPTH = TopTarget_DEPTH
        self.calc_pred_TopTarget_DEPTH = (
            df.groupby([self.UWI_str])[TopTarget_DEPTH].mean().to_frame().reset_index()
        )

    def r2_func(self):
        """
        THINGS GO HERE
        """
        r2_ = r2_score(
            self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH],
            self.calc_pred_Top_Pick_pred_DEPT_pred[self.TopTarget_Pick_pred_DEPT_pred],
        )
        return r2_

    def mean_absolute_error_func(self):
        """
        THINGS GO HERE
        """
        # self.TopTarget_DEPTH
        print(type(self.calc_pred_TopTarget_DEPTH))
        print(type(self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH]))
        print(type(self.calc_pred_Top_Pick_pred_DEPT_pred))
        print(
            type(
                self.calc_pred_Top_Pick_pred_DEPT_pred[
                    self.TopTarget_Pick_pred_DEPT_pred
                ]
            )
        )
        print(type(self.TopTarget_DEPTH))
        print(type(self.TopTarget_Pick_pred_DEPT_pred))
        mean_absolute_error_ = mean_absolute_error(
            self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH],
            self.calc_pred_Top_Pick_pred_DEPT_pred[self.TopTarget_Pick_pred_DEPT_pred],
        )

        # mean_absolute_error_ = mean_absolute_error(self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH], self.calc_pred_Top_Pick_pred_DEPT_pred[self.TopTarget_Pick_pred_DEPT_pred])

        # mean_absolute_error_ = mean_absolute_error(self.calc_pred_TopTarget_DEPTH['TopTarget_DEPTH'], self.calc_pred_Top_Pick_pred_DEPT_pred['TopTarget_Pick_pred_DEPT_pred'])

        return mean_absolute_error_

    def compare_RealTop_vsTopFromRollingMean(self):
        """
        things go here
        """
        new_diff_col = (
            "diff_"
            + str(self.TopTarget_DEPTH)
            + "_-_"
            + str(self.TopTarget_Pick_pred_DEPT_pred)
        )
        self.calc_pred_Top_Pick_pred_DEPT_pred[new_diff_col] = (
            self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH]
            - self.calc_pred_Top_Pick_pred_DEPT_pred[self.TopTarget_Pick_pred_DEPT_pred]
        )
        self.calc_pred_Top_Pick_pred_DEPT_pred[
            self.TopTarget_DEPTH
        ] = self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH]
        #### line below prints histogram
        self.calc_pred_Top_Pick_pred_DEPT_pred.hist(
            column=new_diff_col, bins=80, figsize=(15, 5)
        )

    def run_all(
        self,
        TopTarget_Pick_pred_DEPT_pred,
        TopTarget_DEPTH,
        keepAllWells="no",
        dropIfOnlyClasses=[0],
    ):
        """
        
        """
        ####
        self.optionallyExcludeWellsWithoutStrongPredictions(
            keepAllWells, dropIfOnlyClasses
        )
        self.reduceDFtoOneBestTopPredictionPerWell(TopTarget_Pick_pred_DEPT_pred)
        print("1")
        self.reduceDFtoOriginalTopPerWell(TopTarget_DEPTH)
        print("2")
        #         self.reduceDFtoOneBestTopPredictionPerWell(TopTarget_DEPTH,TopTarget_Pick_pred_DEPT_pred)
        #         print("3")
        #         self.reduceDFtoOriginalTopPerWell(df)
        print("4")
        r2__ = self.r2_func()
        # mean = mean_absolute_error_ = mean_absolute_error(self.calc_pred_TopTarget_DEPTH[self.TopTarget_DEPTH], self.calc_pred_Top_Pick_pred_DEPT_pred[self.TopTarget_Pick_pred_DEPT_pred])
        mean_absolute_error_ = self.mean_absolute_error_func()
        self.compare_RealTop_vsTopFromRollingMean()

        return r2__, mean_absolute_error_, self.calc_pred_Top_Pick_pred_DEPT_pred


def saveRebalanceResultsAsHDFs(df_testPlusRebalTrain_featWithHighCount,train_X,train_y,test_X,
    test_y,
    train_index,
    test_index,
    output_data_inst):
    """
    Takes in 
    Saves 
    Returns 
    """
    ###### Establish file path to save
    load_dir = output_data_inst.base_path_for_all_results + "/" + output_data_inst.path_balance
    load_results_full_file_path = load_dir + "/" + output_data_inst.balance_results_wells_df + output_data_inst.default_results_file_format
    #########################  Write each pandas dataframes to single HDF5 using separate keys to retrieve later
    df_testPlusRebalTrain_featWithHighCount.to_hdf(oad_results_full_file_path, key="preSplitpreBal", mode="w")
    train_X.to_hdf(load_results_full_file_path, key="train_X")
    train_y.to_hdf(load_results_full_file_path, key="train_y")
    test_X.to_hdf(load_results_full_file_path, key="test_X")
    test_y.to_hdf(load_results_full_file_path, key="test_y")
    train_index.to_hdf(load_results_full_file_path, key="train_index")
    test_index.to_hdf(load_results_full_file_path, key="test_index")
    print(
        "finished saving the results of the rebalancing script in the location set in the output class instance. = ",
        load_results_full_file_path,
    )
    return "finished saving the results of the rebalancing script in the location set in the output class instance. = "
