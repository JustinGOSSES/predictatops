


##### import from other modules
from configurationplusfiles import *



input_data_inst = input_data('../data/SPE_006_originalData/OilSandsDB/PICKS.TXT','\t','../data/SPE_006_originalData/OilSandsDB/Logs/*.LAS')

input_data_inst.set_wells_file_path('../data/SPE_006_originalData/OilSandsDB/WELLS.TXT','\t')

input_data_inst.set_gis_file_path('../data/well_lat_lng.csv',',')

input_data_inst.las_folder_path = '../data/SPE_006_originalData/OilSandsDB/Logs/'

print("head of picks df = ",input_data_inst.picks_df.head())

config = configuration()

config.set_must_have_curves(['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT'])

config.set_must_have_tops__list([13000,14000])

config.get_must_have_tops__list()

config.set_top_name_col_in_picks_df('HorID')

print("config.siteID_col_in_picks_df = ",config.siteID_col_in_picks_df)
print("all config is",vars(config))

#return input_data_inst, config
