# -*- coding: utf-8 -*-

##### import statements
import pandas as pd
import numpy as np
import math
import random 



def split_train_test(df_all_Col_preSplit,split_variable,uwi_column_str):
    UWIs = list(df_all_Col_preSplit[uwi_column_str].unique())
    numberOfTrainingWells = math.floor(len(UWIs)*split_variable)
    UWIs_training = random.sample(UWIs, numberOfTrainingWells)
    UWIs_test = [x for x in UWIs if x not in UWIs_training]
    print("train",len(UWIs_training))
    print("test",len(UWIs_test))
    df_all_Col_preSplit_wTrainTest = df_all_Col_preSplit.copy()
    df_all_Col_preSplit_wTrainTest['trainOrTest'] = np.where(df_all_Col_preSplit_wTrainTest[uwi_column_str].isin(UWIs_training), 'train', 'test')
    return df_all_Col_preSplit_wTrainTest

