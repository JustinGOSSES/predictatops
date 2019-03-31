from checkdata import *

#### Configu and input data setup

# input_data_inst = input_data('../data/SPE_006_originalData/OilSandsDB/PICKS.TXT','\t','../data/SPE_006_originalData/OilSandsDB/Logs/*.LAS')

# input_data_inst.set_wells_file_path('../data/SPE_006_originalData/OilSandsDB/WELLS.TXT','\t')

# input_data_inst.set_gis_file_path('../data/well_lat_lng.csv',',')

# input_data_inst.las_folder_path = '../data/SPE_006_originalData/OilSandsDB/Logs/'

# print("head of picks df = ",input_data_inst.picks_df.head())

# config = configuration()

# config.set_must_have_curves(['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT'])

# config.set_must_have_tops__list([13000,14000])

# config.get_must_have_tops__list()

# config.set_top_name_col_in_picks_df('HorID')

# print("config.siteID_col_in_picks_df = ")
# config.siteID_col_in_picks_df

##### Find available tops


from configurationplusfiles_runner import input_data_inst, config
print("test")


tops = TopsAvailable(input_data_inst,config)

print("finding unique tops:")
tops.find_unique_tops_list()

#### Take out wells with no tops, this assumes some data structures that might not exist in your data, so check code!
tops.take_out_wells_with_no_tops()

tops_counts = tops.get_df_of_top_counts_in_picks_df()
print("tops_counts = ",tops_counts)

print("number of wells with any tops:")
tops.get_number_wells_with_any_top()

#### Will print: returning list of wells names that have the required tops. The length of list is : ###  If this number is too small, consider changing the required tops in the configuration object.
test = tops.findWellsWithAllTopsGive()

##### Example use pattern if you just want to initiate Class and run all the functions using variables defined in configruation object
####  This just creates a class instance and then calls run_all()

new_tops2 = TopsAvailable(input_data_inst,config)
wells_with_required_tops = new_tops2.run_all()

print("first well that meets requirements:",wells_with_required_tops[0])


print("number of wells that meet requirements so far:",len(wells_with_required_tops))


print("configuration variables so far, gotten by printing vars(config):",vars(config))


#### Find & understand available curves

curvesInst2 = CurvesAvailable(input_data_inst,config)

curves_results  = curvesInst2.run_all()

curves_results.keys()

print("curves_results['wellsWithWantedCurves'][0:5]",curves_results['wellsWithWantedCurves'][0:5])

print("len(curves_results['wellsWithWantedCurves'])")
len(curves_results['wellsWithWantedCurves'])
print("vars(curvesInst2).keys()",vars(curvesInst2).keys())

curvesInst2.config.threshold_returnCurvesThatArePresentInThisManyWells = 1916

onlyPlentifulCurvesArray = curvesInst2.getCurvesInMinNumberOfWells()
onlyPlentifulCurvesArray

wells_with_tops_and_curves = list(set(wells_with_required_tops).intersection(curves_results['wellsWithWantedCurves']))


print("len(wells_with_tops_and_curves)",len(wells_with_tops_and_curves))

objectOfCurves = curves_results["objectOfCurves"]

wellsWithNeededCurvesList = findWellsWithCertainCurves(objectOfCurves,onlyPlentifulCurvesArray)

print("number of wells with all the required curves is",len(wellsWithNeededCurvesList))

#### NOTE! when we import the wells for real, we should add in the wells that have DEPTH instead of DEPT and rename the curve to DEPT!¶

print(onlyPlentifulCurvesArray)

newCurveList = getCurvesListWithDifferentCurveName(onlyPlentifulCurvesArray,'DEPT','DEPTH')
print("newCurveList",newCurveList)

wellsWithNeededCurvesListButDEPTHinsteadDEPT = findWellsWithCertainCurves(objectOfCurves,newCurveList)
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

#### Hmmm, zero? Let's see if we can get those 7 wells that we know have DEPTH instead of DEPT to appear if we reduce the other curve names?

wellsWithNeededCurvesListButDEPTHinsteadDEPT0 = findWellsWithCertainCurves(objectOfCurves,['GR','DEPTH'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))


wellsWithNeededCurvesListButDEPTHinsteadDEPT1 = findWellsWithCertainCurves(objectOfCurves,['GR','DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT2 = findWellsWithCertainCurves(objectOfCurves,['ILD', 'NPHI', 'GR','DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT3 = findWellsWithCertainCurves(objectOfCurves,['ILD', 'GR', 'DPHI','DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT4 = findWellsWithCertainCurves(objectOfCurves,['ILD', 'GR', 'DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT5 = findWellsWithCertainCurves(objectOfCurves,['ILD', 'GR', 'DEPTH'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT6 = findWellsWithCertainCurves(objectOfCurves,['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT7 = findWellsWithCertainCurves(objectOfCurves,['ILD', 'NPHI', 'GR', 'DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))


#### final try
print("final version:")
wellsWithNeededCurvesList_real = findWellsWithCertainCurves(objectOfCurves,config.must_have_curves_list)
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesList_real))


print("wellsWithNeededCurvesList_real, first 3 wells:",wellsWithNeededCurvesList_real[0:3])

#### Make list of wells that includes both the minimum required curves & minimum required tops
#### These two lists are different. One is SITEID the other is LAS file name. We'll convert them in the function below and find the ones in common and returnt that as a new list of wells.


#WellsWithGivenTopsCurves = findWellsWithGivenTopsCurves(input_data_inst.wells_df,wells_with_required_tops,wellsWithNeededCurvesList_real)

#print("len(WellsWithGivenTopsCurves)",len(WellsWithGivenTopsCurves))



wells_with_required_tops_and_curves_list = list(set(wells_with_required_tops).intersection(wellsWithNeededCurvesList_real))
print("length wells_test",len(wells_with_required_tops_and_curves_list))
print("wells_test = ",wells_with_required_tops_and_curves_list)
#print("wells with needed curves list real",wellsWithNeededCurvesList_real)
#print("wells wells_with_required_tops",wells_with_required_tops)

#### NOW LETS SAVE RESULTS

print("type of wells_with_required_tops_and_curves_list",type(wells_with_required_tops_and_curves_list))

wells_with_required_tops_and_curves_list_df = pd.DataFrame(np.array(wells_with_required_tops_and_curves_list), columns = ["wells"])

print("type",type(wells_with_required_tops_and_curves_list_df))


file_path_for_results = config.results_path+"/"+config.availableData_path+"/"+"wells_with_required_tops_and_curves_list.h5"
print("will now save results in hdf5 file in:",file_path_for_results)
key_for_file_path_for_results = 'wellsWTopsCurves'
print("key for hdf file is",key_for_file_path_for_results)

wells_with_required_tops_and_curves_list_df.to_hdf(file_path_for_results, key=key_for_file_path_for_results, mode='w')