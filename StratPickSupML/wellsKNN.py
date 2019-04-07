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
import os
import folium
#print("folium",folium.__version__)
import branca.colormap as cm
import os
import math
#print("welly",welly.__version__)
import re

##### Load pick, pick dictionary, well information, and well location via csv and text file #####
# picks_dic = pd.read_csv('../../../SPE_006_originalData/OilSandsDB/PICKS_DIC.TXT',delimiter='\t')
# picks = pd.read_csv('../../../SPE_006_originalData/OilSandsDB/PICKS.TXT',delimiter='\t')
# wells = pd.read_csv('../../../SPE_006_originalData/OilSandsDB/WELLS.TXT',delimiter='\t')
# gis = pd.read_csv('../../../well_lat_lng.csv')


##### Dataframe of well curves data created in load notebook #####
# loaded_wells_dir = '../loadLAS/'
# loaded_wells_splitTrainTest_dir = '../splitTrainTest/'
# loaded_wells_splitTrainTest_df = 'df_all_wells_noKNNorFeatures_wTrainSplit_20180927_c.h5'


##### h5 file to write to at end: #####
#h5_name_wells_curves_picks_knn_nofeature = 'wells_curves_picks_knn_nofeatures_20190928_a.h5'


##### Give top pick code that we want to predict and give base pick code that we want to assume we have #####
# ##### Dataframe of well curves data created in load notebook #####
# #### top pick code we are going to predict
# picks_targetTop=picks[picks['HorID']==13000]
# #### base pick code we are going to assume we have
# picks_targetBase=picks[picks['HorID']==14000]

#### Note: these need to be in this order as we'll assume the second one will be written as 'HorID_x' by pandas as two columns can't have the same name

##### Merge information from the various files into a pandas dataframe #####
# df_new = pd.merge(wells, picks_targetTop, on='SitID')
# df_paleoz = pd.merge(wells, picks_targetBase, on='SitID')
# df_gis = pd.merge(df_paleoz, gis, on='SitID')
# df_new=pd.merge(df_gis, df_new, on='SitID')
# df_new.head()

