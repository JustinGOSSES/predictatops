
# -*- coding: utf-8 -*-

#### Import
from load import *
from checkdata_runner import checkdata_path_results
from configurationplusfiles_runner import input_data_inst, config, output_data_inst

################ path_to_wells,file_ending ###################
check_dir = output_data_inst.base_path_for_all_results+ "/" + output_data_inst.path_checkData

checkdata__file_path_for_results = checkdata_path_results

max_numb_wells_to_load = config.max_numb_wells_to_load


################ Load File of well names saved from running checkdata functions ###################


wellNames_wTopsCuves_toLoad  = pd.read_hdf(checkdata__file_path_for_results)
print("wellNames_wTopsCuves_toLoad = ",wellNames_wTopsCuves_toLoad)
#saved_wells_df_name_h5


#### Establish where to get files from and where to save
#wellNames_wTopsCuves_toLoad = 'WellNamesWithGivenTopsCurves_20180927_vC.pkl'
#saved_wells_df_name_h5 = 'df_all_wells_noKNNorFeatures.h5'


#### Load list of wells we want that we created in the checkdata step:
###### but change from pickle to h5
#WellsWithGivenTopsCurves_201809_vA = pickle.load( open( check_dir+wellNames_wTopsCuves_toLoad, "rb" ) )

print("length of wells we want is:",len(wellNames_wTopsCuves_toLoad))

print("examples of well names we'll try to find are:",wellNames_wTopsCuves_toLoad[0:4])


path_to_wells = input_data_inst.las_folder_path
file_ending  = input_data_inst.well_format



#### Changes format of well list into a pandas dataframe with one column called "UWI_file".
#wells_df = makeDF(wellNames_wTopsCuves_toLoad)
wells_df = wellNames_wTopsCuves_toLoad
print("info for wells_df: type, columns, and length = ",type(wells_df),wells_df.columns,len(wells_df))

number_of_wells_in_given_folder = find_number_well_files_in_a_folder(path_to_wells,file_ending)
print("number of wells found in ",path_to_wells,"*",file_ending," folder is ",number_of_wells_in_given_folder)

#### Loading the wells for real now
initial_well_dict = load_all_wells_in(wells_df,max_numb_wells_to_load,path_to_wells,file_ending)

#dict_of_well_df = compute(initial_well_dict)
dict_of_well_df = initial_well_dict
dict_of_well_df_0 = dict_of_well_df[0]
print(type(dict_of_well_df_0),"type dict_of_well_df_0")
#print("dict_of_well_df_0",dict_of_well_df_0)
list_of_failed_wells = initial_well_dict[1]

print("length of wells we have determined have the tops and curves we desire is:",len(wellNames_wTopsCuves_toLoad))
print("len(list_of_failed_wells)",len(list_of_failed_wells))
print("len(dict_of_well_df[0])",len(dict_of_well_df[0]))
print("length of all seen wells, which is failed and completed wells combined",len(set(list_of_failed_wells))+len(dict_of_well_df[0]))

print("type(dict_of_well_df) = ",(type(dict_of_well_df)))

df_1 = turn_dict_of_well_dfs_to_single_df(dict_of_well_df_0)

print("we now has all the wells we want in a single dataframe with ",len(df_1['UWI'].unique())," unique UWI identifiers")

saved_wells_df_name_h5 = output_data_inst.base_path_for_all_results+"/"+output_data_inst.path_load+"/"+output_data_inst.loaded_results_wells_df+output_data_inst.default_results_file_format


#### Save dataframe as hdf
df_1.to_hdf(saved_wells_df_name_h5, key='df', mode='w')