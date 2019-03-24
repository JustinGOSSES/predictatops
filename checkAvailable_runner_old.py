from checkAvailableData import *


input_data_ = input_data('data/SPE_006_originalData/OilSandsDB/PICKS.TXT','\t','data/SPE_006_originalData/OilSandsDB/Logs/*.LAS')

input_data_.set_wells_file_path('data/SPE_006_originalData/OilSandsDB/WELLS.TXT','\t')

input_data_.set_gis_file_path('data/well_lat_lng.csv',',')

input_data_.set_must_have_curves(['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT'])

wells_wTopsCuves_toLoad = 'WellNamesWithGivenTopsCurves_20180927_vC.pkl'


curvesMustHave = ['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT']

picks_dic = pd.read_csv('data/SPE_006_originalData/OilSandsDB/PICKS_DIC.TXT',delimiter='\t')
picks = pd.read_csv('data/SPE_006_originalData/OilSandsDB/PICKS.TXT',delimiter='\t')
wells = pd.read_csv('data/SPE_006_originalData/OilSandsDB/WELLS.TXT',delimiter='\t')
gis = pd.read_csv('data/well_lat_lng.csv')

listOfTops = picks_dic.HorID.unique()

print("listOfTops",listOfTops)

#### produces dataframe with no picks that have a value of zero
noZeroPicks = picks[picks.Pick != 0]
#### produces dataframe that doesn't have any picks with a quality of negative one, meaning not to be trusted or present
noNullPicks = noZeroPicks[noZeroPicks.Quality != -1]
#### produces dataframe of horID and counts of non-zero,non-null picks
pick_counts = noNullPicks.groupby('HorID').SitID.count()

print("pick_counts",pick_counts)

wells_with_picks_array = picks.SitID.unique()
print("number of wells with picks of some sort is: ",len(wells_with_picks_array))


topsMustHave = [13000,14000]


wells_with_all_given_tops = findWellsWithAllTopsGive(topsMustHave,picks)

print("len(wells_with_all_given_tops)",len(wells_with_all_given_tops))

las_path = '../../../SPE_006_originalData/OilSandsDB/Logs/*.LAS'

objectOfCurves = findAllCurvesInGivenWells(las_path)


#print("first well in object of curves",list(objectOfCurves.keys()))

countsOfCurves = countsOfCurves(objectOfCurves)


print("countsOfCurves",countsOfCurves)

minNumberCurves = 2000

plentifulCurves = getCurvesInMinNumberOfWells(minNumberCurves,countsOfCurves)

print("plentifulCurves ",plentifulCurves)

wellsWithNeededCurvesList = findWellsWithCertainCurves(objectOfCurves,plentifulCurves)


print("number of wells with all the required curves is",len(wellsWithNeededCurvesList))

newCurveList = getCurvesListWithDifferentCurveName(plentifulCurves,'DEPT','DEPTH')
print("newCurveList",newCurveList)

wellsWithNeededCurvesListButDEPTHinsteadDEPT = findWellsWithCertainCurves(objectOfCurves,newCurveList)
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))

wellsWithNeededCurvesListButDEPTHinsteadDEPT = findWellsWithCertainCurves(objectOfCurves,['GR','DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))


wellsWithNeededCurvesListButDEPTHinsteadDEPT = findWellsWithCertainCurves(objectOfCurves,['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))



wellsWithNeededCurvesListButDEPTHinsteadDEPT = findWellsWithCertainCurves(objectOfCurves,['ILD', 'NPHI', 'GR', 'DEPT'])
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesListButDEPTHinsteadDEPT))



wellsWithNeededCurvesList_real = findWellsWithCertainCurves(objectOfCurves,curvesMustHave)
print("number of wells with all the required curves but DEPTH instead of DEPT is",len(wellsWithNeededCurvesList_real))


print("len(wells_with_all_given_tops)",len(wells_with_all_given_tops))

print(len(wellsWithNeededCurvesList_real))


new_wells = wells.set_index('SitID').T.to_dict('list')
print("new_wells",new_wells)


WellsWithGivenTopsCurves = findWellsWithGivenTopsCurves(wells,wells_with_all_given_tops,wellsWithNeededCurvesList_real)


print("len(WellsWithGivenTopsCurves)",len(WellsWithGivenTopsCurves))





