# -*- coding: utf-8 -*-

##### import from other python files in this package #####
from wellKNN import *
from configurationplusfiles_runner import input_data_inst, config, output_data_inst





##### path to input file ######
split_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_split
split_file = output_data_inst.split_results_wells_df
ending = output_data_inst.default_results_file_format
full_path_to_split_results = split_dir+"/"+split_file+ending

################ Load wells df saved from running split functions ###################
################ This file is wells loaded with no features but does have a column for train test split ###################

wells_df_from_split  = pd.read_hdf(full_path_to_split_results)




