# -*- coding: utf-8 -*-


#### Import
import pandas as pd


from split import *
#from load_runner import saved_wells_df_name_h5
from configurationplusfiles_runner import input_data_inst, config, output_data_inst

################ path_to_wells,file_ending ###################
load_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_load
load_filename = output_data_inst.load_results_wells_df_onlywanted 
load_results_full_file_path = load_dir+"/"+load_filename+output_data_inst.default_results_file_format

#saved_wells_df_name_h5 = saved_wells_df_name_h5

max_numb_wells_to_load = config.max_numb_wells_to_load


################ Load File of well names saved from running checkdata functions ###################
################ This file is wells loaded but no features or train test split yet ###################

wells_df_from_load  = pd.read_hdf(load_results_full_file_path)

################ File that will be written at the end ###################



################ configuration ###################
split_variable = config.split_traintest_percent

################ code ###################
df_all_Col_preSplit_wTrainTest = split_train_test(wells_df_from_load,split_variable,config.UWI)

saved_split_wells_df_name_h5 = output_data_inst.base_path_for_all_results+"/"+output_data_inst.path_split+"/"+output_data_inst.split_results_wells_df+output_data_inst.default_results_file_format


#### Save dataframe as hdf
df_all_Col_preSplit_wTrainTest.to_hdf(saved_split_wells_df_name_h5, key='df', mode='w')

