# -*- coding: utf-8 -*-


################ import from other python files in this package ###################
from trainclasses import *
from configurationplusfiles_runner import input_data_inst, config, output_data_inst
from main import get_df_results_from_step_X, getMainDFsavedInStep, load_prev_results_at_path



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





ML1 = ML_obj_class(output_data_inst)

# ML1.knn_dir

ML1.load_data_for_ml()
ML1.dropNeighbors_ObjCol("Neighbors_Obj")

print("printing the preSplitpreBal df head that was saved in the balance part of the workflow.")
ML1.preSplitpreBal.head()

# ML1.preSplitpreBal = ML1.preSplitpreBal[0:50000]
# ML1.train_X = ML1.train_X[0:50000]
# ML1.train_y = ML1.train_y[0:50000]
# ML1.test_X = ML1.test_X[0:50000]
# ML1.test_y = ML1.test_y[0:50000]
print("ML1.train_X.columns",ML1.train_X.columns)

print("Now starting to make the model. If none given, parameters that worked well for the top McMurray pick will be used.")
print("default model parameters provided are: gamma=0, reg_alpha=0.3, max_depth=6, subsample=0.8, colsample_bytree= 0.8, n_estimators= 300, learning_rate= 0.03, min_child_weight= 3,n_jobs=8")

model = ML1.init_XGBoost_withSettings()

print("now fitting the model to the training data:")
model.fit(ML1.train_X,ML1.train_y)

############ just to show what model contains a bit  ###########

print("just to show what model contains a bit:")

print("type(model)",type(model))

print("model stats",model)

print("model.subsample",model.subsample)

############   Optionally loading the already trained model here if it already exists locally.   ############ 
############   It can take quite a while to fit the model, so sometimes easier to save a copy and then load it.   ############ 

######################### WRITE FUNCTION FOR THIS !!!!!! ####################
######################### Something like: model = pickle.load(open("classModel_20181122a.pickle.dat", "rb")) & print(type(model))

#model = pickle.load(open("classModel_20181122a.pickle.dat", "rb")) & print(type(model))

saveTrainClassesResultsAsPickle(model,ML1,output_data_inst)

