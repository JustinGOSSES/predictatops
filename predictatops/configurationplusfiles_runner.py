# -*- coding: utf-8 -*-


##### import from other modules
from configurationplusfiles import *



input_data_inst = input_data('../data/Mannville_input_data/v0.0.0-alpha/OilSandsDB/PICKS.TXT','\t','../data/SPE_006_originalData/OilSandsDB/Logs/*.LAS')

input_data_inst.set_wells_file_path('../data/Mannville_input_data/v0.0.0-alpha/OilSandsDB/WELLS.TXT','\t')

input_data_inst.set_gis_file_path('../data/Mannville_input_data/v0.0.0-alpha/well_lat_lng.csv',',')

input_data_inst.las_folder_path = '../data/Mannville_input_data/v0.0.0-alpha/OilSandsDB/Logs/'

print("head of picks df = ",input_data_inst.picks_df.head())

#### Initiates an object  from the output data class and then creates all the directories for intermediate and final output files
output_data_inst =output_data()

#### CHANGE base_path_for_all_results, was '../results'
output_data_inst.base_path_for_all_results = '../results_higherBlanceAndLowerWindows_20190517'

output_data_inst.make_all_directories()



config = configuration()

config.set_must_have_curves(['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT'])

config.set_must_have_tops__list([13000,14000])

#### Changed for may 17th
#### this change performed worse than default:
## config.curve_windows_for_rolling_features = [3,5,11,21]
#### default is [5,7,11,21]
config.rebalanceClassZeroMultiplier = 120
config.rebalanceClass95Multiplier = 60


config.get_must_have_tops__list()

config.set_top_name_col_in_picks_df('HorID')

print("config.siteID_col_in_picks_df = ",config.siteID_col_in_picks_df)
print("all config is",vars(config))

#return input_data_inst, config
