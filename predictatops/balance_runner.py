# -*- coding: utf-8 -*-

##### import from other modules
from balance import *

##### BASED ON notebook PreML_ClassRebalence_FeatureSelection_Prep_20181003_vF in Mannville repo
##### preceeded by feature creation notebooks
##### (without Dask)


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


# #### Had to change display options to get this to print in full!
# #pd.set_option('display.height', 1000)
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.options.display.max_colwidth = 100000