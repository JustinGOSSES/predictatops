import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
# %matplotlib inline

import welly
from welly import Well
import lasio
import glob
import pickle
import math
import re

import os
# env = %env


class input_data():
    """doc string"""
    def __init__(self, picks_file_path, picks_delimiter_str,path_to_logs_str):
        #### Default initiation = ('../../../SPE_006_originalData/OilSandsDB/PICKS.TXT','\t','../../../SPE_006_originalData/OilSandsDB/Logs/*.LAS')
        #### Only things that are mandatory on initiation are below
        self.picks_file_path = picks_file_path #### example = '../../../SPE_006_originalData/OilSandsDB/PICKS.TXT'
        self.picks_delimiter_str = picks_delimiter_str  #### example = '\t'
        self.picks_df = pd.read_csv(self.picks_file_path,delimiter=picks_delimiter_str)
        self.logs_path_to_folder = path_to_logs_str #### example = '../../../SPE_006_originalData/OilSandsDB/Logs/*.LAS'
        
        #### non-mandatory attributes, defaults should work for the example dataset. Can be changed with set functions below
        self.wells_file_path = '../../../SPE_006_originalData/OilSandsDB/WELLS.TXT'
        self.wells_file_path_delimiter = '\t'
        self.gis_file_path = '../../../well_lat_lng.csv'
        self.gis_file_path_delimiter = ','
        wells_wTopsCuves_toLoad = 'WellNamesWithGivenTopsCurves_defaultFileName.pkl'
       
        #### 
        self.wells_df = None
        self.gis_df = None
        
        #### Choices
        self.must_have_curves_list = ['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT']
   
    def load_wells_file(self):
        """ load wells file into pandas dataframe """
        self.wells_df = pd.read_csv(self.wells_file_path,delimiter=self.wells_file_path_delimiter)
        return self.wells_df
    
    def load_gis_file(self):
        """ load wells file into pandas dataframe """
        self.gis_df = pd.read_csv(self.gis_file_path,delimiter=self.gis_file_path_delimiter)
        return self.gis_df
        
    def set_wells_file_path(self,wells_file_path_str,wells_file_delimiter):
        """ set wells file path as attribute of object and returns wells data frame using load_well_file. Can be txt, tsv, or csv"""
        self.wells_file_path = wells_file_path_str
        self.wells_file_path_delimiter = wells_file_delimiter
        return self.load_wells_file()
    
    def set_gis_file_path(self,gis_file_path_str,gis_file_path_delimiter):
        """ set wells file path as attribute of object and returns wells data frame using load_well_file. Can be txt, tsv, or csv"""
        self.gis_file_path = gis_file_path_str
        self.gis_file_path_delimiter = gis_file_path_delimiter
        return self.load_gis_file()
    
    def set_must_have_curves(self,must_have_curves_in_list):
        """doc string goes here"""
        self.must_have_curves_list = must_have_curves_in_list
        print("must have curve list is: ",must_have_curves_in_list)

def findWellsThatHaveCertainTop(top,picks):
    #### Takes in top
    #### Returns a list of wells with the given top
    #print(top)
    rows_with_picks = picks[picks.Quality != 0]
    rows_with_picks = rows_with_picks[rows_with_picks.Quality != -1]
    #print(rows_with_picks[0:4])\
    
    test = rows_with_picks.loc[rows_with_picks['HorID'] == top]
    #test['Pick'].replace(r'\s+', np.nan, regex=True)
    test['Pick'].replace('', np.nan, inplace=True)
    print(test)
    rows_with_that_top = list(rows_with_picks.loc[rows_with_picks['HorID'] == top].dropna().SitID.unique())
    #print("before return",rows_with_that_top)
    return rows_with_that_top


def findWellsWithAllTopsGive(tops,picks):
    #### Takes in a list of tops
    #### Returns a list of wells that include all of those tops. If only one top occurs, well is not included
    list_of_wells_with_tops = []
    for top in tops:
        list_of_wells_with_tops.append(findWellsThatHaveCertainTop(top,picks))
#     for item in 
    print(len(list_of_wells_with_tops))
    list_of_wells_with_tops =list(set(list_of_wells_with_tops[0]).intersection(list_of_wells_with_tops[1]))
    
#     print(len(list_of_wells_with_tops))
#     wells = []
    
#     for item in list_of_wells_with_tops:
#         wells = wells+item
#     result = set(wells)
#     for s in list_of_wells_with_tops[1:]:
#         result.intersection_update(s)=
#    result = list(result)
    return list_of_wells_with_tops


def findAllCurvesInGivenWells(path):
    objectOfCurves = {}
    for fn in glob.glob(path):
        las = lasio.read(fn, ignore_data=True)
        mnemonics = [c.mnemonic for c in las.curves]
        fnShort = fn.replace("../../../SPE_006_originalData/OilSandsDB/Logs/","")
        objectOfCurves[fnShort] = mnemonics
    #print(fn + '\n\t' + '\n\t'.join(mnemonics))
    return objectOfCurves


def countsOfCurves(objectOfCurves):
    listOfListOfCurves = objectOfCurves.values()
    startList = []
    for listI in listOfListOfCurves:
        startList = startList+listI
    uniq_CurvesList = set(startList)
    countsOfCurves = {}
    for eachCurve in uniq_CurvesList:
        countsOfCurves[eachCurve] = startList.count(eachCurve)
    return countsOfCurves


def getCurvesInMinNumberOfWells(minNumberCurves,countsOfCurves):
    #### Takes in a minmum number of wells that need to have specific curves and an object where keys are curve names and values is the count of that curves across all wells.
    #### Returns an array of curve names that are found in at least the given number of wells.
    curvePlusCountArray = countsOfCurves.items()
    onlyPlentifulCurvesArray = []
    for curve in curvePlusCountArray:
        if curve[1] > minNumberCurves:
            onlyPlentifulCurvesArray.append(curve[0])
    return onlyPlentifulCurvesArray


def findWellsWithCertainCurves(objectOfCurves,plentifulCurves):
    #### Function takes in an object with keys that are well names and values that are all curves in that well and as the second argument an array of plentiful curves expected to be in every well
    #### Function returns an array of wells that have the specified curves in the second argument.
    wellsWithWantedCurves = []
    for eachWell in objectOfCurves.keys():
        if set(plentifulCurves).issubset(objectOfCurves[eachWell]):
            wellsWithWantedCurves.append(eachWell)
    return wellsWithWantedCurves

def getCurvesListWithDifferentCurveName(originalCurveList,origCurve,newCurve):
    #### Takes in list of curves, curve name to be replaced, and curve name to replace with.
    #### Returns a list with the orginal and new curve names switched in the given curve list
    plentifulCurves_wDEPTH = originalCurveList.copy()
    plentifulCurves_wDEPTH.remove(origCurve)
    plentifulCurves_wDEPTH.append(newCurve)
    return plentifulCurves_wDEPTH


def findWellsWithGivenTopsCurves(wells,wells_with_all_given_tops,wellsWithNeededCurvesList_real):
    new_wells = wells.set_index('SitID').T.to_dict('list')
    #print("new_wells",new_wells)
    for key in new_wells:
        new_wells[key].append(new_wells[key][1].replace("/","-")+".LAS") 
    print("new_wells",new_wells)
    print(len(new_wells))
    new_wells_with_all_given_tops = []
    for well in wells_with_all_given_tops:
        new_wells_with_all_given_tops.append(new_wells[well][2])
    return list(set(new_wells_with_all_given_tops).intersection(wellsWithNeededCurvesList_real))

