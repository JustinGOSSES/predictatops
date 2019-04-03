##### Classes


from load import *

#### Import configuration, input, and output helpers
knn_dir = "../WellsKNN/"
check_dir = "../CheckAvailableData/"

#path_to_wells,file_ending

#max_numb_wells



########## NEED TO DO MORE HERE USING CONFIGURATION FILES ETC.




#### Establish where to get files from and where to save
wellNames_wTopsCuves_toLoad = 'WellNamesWithGivenTopsCurves_20180927_vC.pkl'
saved_wells_df_name_h5 = 'df_all_wells_noKNNorFeatures_20180927_a.h5'


#### Load list of wells we want that we created in the checkdata step:
###### but change from pickle to h5
WellsWithGivenTopsCurves_201809_vA = pickle.load( open( check_dir+wellNames_wTopsCuves_toLoad, "rb" ) )

print("length of wells we want is:",len(WellsWithGivenTopsCurves_201809_vA))

print("examples of well names we'll try to find are:",WellsWithGivenTopsCurves_201809_vA[0:4])

#### Changes format of well list into a pandas dataframe with one column called "UWI_file".
wells_df = makeDF(WellsWithGivenTopsCurves_201809_vA)

number_of_wells_in_given_folder = find_number_well_files_in_a_folder(path_to_wells,file_ending)
print("number of wells found in ",path_to_wells,"*",file_ending," folder is ",number_of_wells_in_given_folder)

#### Loading the wells for real now
initial_well_dict = load_all_wells_in(wells_df)
dict_of_well_df = compute(initial_well_dict)
dict_of_well_df = dict_of_well_df[0]
list_of_failed_wells = initial_well_dict[1]

print("len(list_of_failed_wells)",len(list_of_failed_wells))
print("len(dict_of_well_df[0])",len(dict_of_well_df[0]))
print("length of all seen wells, which is failed and completed wells combined",len(set(list_of_failed_wells))+len(dict_of_well_df[0]))

print("type type(dict_of_well_df) = ",type(type(dict_of_well_df)))

df_1 = turn_dict_of_well_dfs_to_single_df(dictOfWellDf)

print("we now has all the wells we want in a single dataframe with ",len(df_1['UWI'].unique())," unique UWI identifiers")




#### Save dataframe as hdf
df_1.to_hdf(saved_wells_df_name_h5, key='df', mode='w')