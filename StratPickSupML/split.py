
##### import statements
import pandas as pd
import numpy as np
import itertools
import math
import random 

##### IMPORT CONFIGURATION

##### HOW IS THIS CONFIGURATION DONE IF PEOPLE WANT TO SET IT BY HAND?????

knn_dir = "../WellsKNN/"
load_dir = "../loadLAS/"
features_dir = "../createFeatures/"
check_dir = "../CheckAvailableData/"
loadLas_dir = "../loadLAS/"


#### File with wells loaded but not features or train test split yet

file_with_wells = 'df_all_wells_noKNNorFeatures_20180927_a.h5'

##### File to write to at end =

h5_filename_df_wells_wTrainTestSplitCol = 'df_all_wells_noKNNorFeatures_wTrainSplit_20180927_c.h5'

#### split variable
split_variable = 0.8



################# Load


df_all_Col_preSplit = pd.read_hdf(load_dir+file_with_wells, 'df')


#### Split data into train & test on a well by well basis, not row basis¶
UWIs = list(df_all_Col_preSplit['UWI'].unique())

numberOfTrainingWells = math.floor(len(UWIs)*split_variable)
numberOfTrainingWells

#### Randomly select that number of UWIs for training and the ones left for test

UWIs_training = random.sample(UWIs, numberOfTrainingWells)

UWIs_test = [x for x in UWIs if x not in UWIs_training]

#### Print to make sure things make sense

print("train length = ",len(UWIs_training))
print("test length = ",len(UWIs_test))

df_all_Col_preSplit_wTrainTest = df_all_Col_preSplit.copy()

df_all_Col_preSplit_wTrainTest['trainOrTest'] = np.where(df_all_Col_preSplit_wTrainTest['UWI'].isin(UWIs_training), 'train', 'test')

#### optional print
df_all_Col_preSplit_wTrainTest.tail()

#### Save to file

df_all_Col_preSplit_wTrainTest.to_hdf(h5_filename_df_wells_wTrainTestSplitCol, key='df', mode='w')

